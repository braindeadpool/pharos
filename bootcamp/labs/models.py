from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from bootcamp.devices.models import Device

import markdown

#todo add list of team members for a Project

@python_2_unicode_compatible
class Lab(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=4000)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    
    mgr_id = models.ForeignKey(User, related_name="lab_manager")
    date = models.DateTimeField(auto_now_add=True)

    institution = models.CharField(max_length=200, null=True, blank=True) 
    building = models.CharField(max_length=200, null=True, blank=True) 
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    
    

    class Meta:
        verbose_name = _("Lab")
        verbose_name_plural = _("Labs")
        ordering = ("-create_date",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Lab, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s %s" % (self.pk, self.name.lower())
            self.slug = slugify(slug_str)
        super(Lab, self).save(*args, **kwargs)

    def get_description_as_markdown(self):
        return markdown.markdown(self.description, safe_mode='escape')

    @staticmethod
    def get_published():
        labs = Lab.objects.filter(status=Lab.PUBLISHED)
        return labs

    @staticmethod
    def get_published_by_user(user):
        labs = Lab.objects.filter(status=Lab.PUBLISHED, mgr_id = user)
        return labs

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                t, created = Tag.objects.get_or_create(tag=tag.lower(),
                                                       lab=self)

    def get_tags(self):
        return Tag.objects.filter(lab=self)
    
    def delete_tags(self):
        Tag.objects.filter(lab=self).delete()
    
    def get_summary(self):
        if len(self.description) > 255:
            return '{0}...'.format(self.description[:255])
        else:
            return self.description

    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')

    

@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=50)
    lab = models.ForeignKey(Lab)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        unique_together = (('tag', 'lab'),)
        index_together = [['tag', 'lab'], ]

    def __str__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        tags = Tag.objects.all()
        count = {}
        for tag in tags:
            if tag.lab.status == Lab.PUBLISHED:
                if tag.tag in count:
                    count[tag.tag] = count[tag.tag] + 1
                else:
                    count[tag.tag] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]
    
class Device(models.Model):
    #Lab Manager ID
    manager = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    #Device Name
    device = models.ForeignKey(Device)
    name = models.CharField(max_length=200, null=True, blank=True)
    lab = models.ForeignKey(Lab)
    desciption = models.CharField(max_length=1000, null=True, blank=True) 
    requestor = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name + "  " + self.lab.name


