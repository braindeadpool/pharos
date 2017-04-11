from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from bootcamp.devices.models import Device
from bootcamp.projects.models import Project

import markdown


@python_2_unicode_compatible
class Sample(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )

    name = models.CharField(max_length=255)
    identification = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=4000)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True,
                                    related_name="+")
    project = models.ForeignKey(Project)
    devices = models.ManyToManyField(Device, blank=True, null=True)

    class Meta:
        verbose_name = _("Sample")
        verbose_name_plural = _("Samples")
        ordering = ("-create_date",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Sample, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s %s" % (self.pk, self.name.lower())
            self.slug = slugify(slug_str)
        super(Sample, self).save(*args, **kwargs)

    def get_description_as_markdown(self):
        return markdown.markdown(self.description, safe_mode='escape')

    @staticmethod
    def get_published():
        samples = Sample.objects.filter(status=Sample.PUBLISHED)
        return samples

    @staticmethod
    def get_published_by_user(user):
        samples = Sample.objects.filter(status=Sample.PUBLISHED, create_user=user)
        return samples

    def get_project(self):
        return self.project

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                t, created = SampleTag.objects.get_or_create(tag=tag.lower(),
                                                             sample=self)

    def get_tags(self):
        return SampleTag.objects.filter(sample=self)

    def delete_tags(self):
        SampleTag.objects.filter(sample=self).delete()

    def get_summary(self):
        if len(self.description) > 255:
            return '{0}...'.format(self.description[:255])
        else:
            return self.description

    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')

    def get_comments(self):
        return SampleComment.objects.filter(sample=self)


@python_2_unicode_compatible
class SampleTag(models.Model):
    tag = models.CharField(max_length=50)
    sample = models.ForeignKey(Sample)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        unique_together = (('tag', 'sample'),)
        index_together = [['tag', 'sample'], ]

    def __str__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        tags = SampleTag.objects.all()
        count = {}
        for tag in tags:
            if tag.sample.status == Sample.PUBLISHED:
                if tag.tag in count:
                    count[tag.tag] = count[tag.tag] + 1
                else:
                    count[tag.tag] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]


@python_2_unicode_compatible
class SampleComment(models.Model):
    sample = models.ForeignKey(Sample)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _("Sample Comment")
        verbose_name_plural = _("Sample Comments")
        ordering = ("date",)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.sample.name)
