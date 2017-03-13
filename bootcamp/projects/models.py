from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from bootcamp.samples.models import Sample, Device

import markdown


@python_2_unicode_compatible
class Project(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=4000)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True,
                                    related_name="+")
    devices = models.ManyToManyField(Device, blank=True, null=True)
    samples = models.ManyToManyField(Sample, blank=True, null=True)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ("-create_date",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Project, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s %s" % (self.pk, self.title.lower())
            self.slug = slugify(slug_str)
        super(Project, self).save(*args, **kwargs)

    def get_description_as_markdown(self):
        return markdown.markdown(self.description, safe_mode='escape')

    @staticmethod
    def get_popular_authors(projects = None):
        if projects is None:
            projects = Project.objects.all()
        count = {}
        for project in projects:
            if project.status == Project.PUBLISHED:
                if project.create_user in count:
                    count[project.create_user] = count[project.create_user] + 1
                else:
                    count[project.create_user] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]

    @staticmethod
    def get_published():
        projects = Project.objects.filter(status=Project.PUBLISHED)
        return projects

    @staticmethod
    def get_published_by_user(user):
        projects = Project.objects.filter(status=Project.PUBLISHED, create_user=user)
        return projects

    @staticmethod
    def get_collaborated_by_user(user):
        all_projects = Project.objects.filter(status=Project.PUBLISHED)
        projects = []
        for project in all_projects:
            collaborators = [x.user for x in project.get_collaborators()]
            if user in collaborators:
                projects.append(project)
        return projects

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                t, created = Tag.objects.get_or_create(tag=tag.lower(),
                                                       project=self)

    def get_tags(self):
        return Tag.objects.filter(project=self)

    def delete_tags(self):
        Tag.objects.filter(project=self).delete()

    def delete_collaborators(self):
        Collaborator.objects.filter(project=self).delete()

    def get_collaborators(self):
        return Collaborator.objects.filter(project=self)

    def get_devices(self):
        return self.devices.all()

    def get_materials(self):
        all = Material.objects.filter(project=self)
        to_return = []
        print all
        for each in all:
            to_return.append(each)
        print "the materials are"
        print to_return
        return to_return

    def get_samples(self):
        all = self.samples.all()
        to_return = []
        print all
        for each in all:
            to_return.append(each)
        print "the samples are"
        print to_return
        return to_return

    def get_collaborators_comma_delimited(self):
        all = Collaborator.objects.filter(project=self)
        to_return = []
        for each in all:
            to_return.append(each.user.first_name + " " + each.user.last_name)
        return ", ".join(to_return)

    def get_summary(self):
        if len(self.description) > 255:
            return '{0}...'.format(self.description[:255])
        else:
            return self.description

    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')

    def get_comments(self):
        return ProjectComment.objects.filter(project=self)


@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=50)
    project = models.ForeignKey(Project)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        unique_together = (('tag', 'project'),)
        index_together = [['tag', 'project'], ]

    def __str__(self):
        return self.tag

    @staticmethod
    def get_popular_tags(projects = None):
        tags = Tag.objects.all()
        count = {}
        if projects is None:
            for tag in tags:
                if tag.project.status == Project.PUBLISHED:
                    if tag.tag in count:
                        count[tag.tag] = count[tag.tag] + 1
                    else:
                        count[tag.tag] = 1
            sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
            return sorted_count[:20]
        else:
            for tag in tags:
                if tag.project in projects and tag.project.status == Project.PUBLISHED:
                    if tag.tag in count:
                        count[tag.tag] = count[tag.tag] + 1
                    else:
                        count[tag.tag] = 1
            sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
            return sorted_count[:20]


@python_2_unicode_compatible
class ProjectComment(models.Model):
    project = models.ForeignKey(Project)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _("Project Comment")
        verbose_name_plural = _("Project Comments")
        ordering = ("date",)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.project.title)


@python_2_unicode_compatible
class Collaborator(models.Model):
    project = models.ForeignKey(Project)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    @staticmethod
    def get_published_by_user(userid):
        objs = Collaborator.objects.filter(user=userid)
        projects = [x.project for x in objs if (x.project.status == Project.PUBLISHED)]
        return projects

    class Meta:
        verbose_name = _("Collaborator")
        verbose_name_plural = _("Collaborators")
        ordering = ("user",)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.project.title)


class Material(models.Model):
    project = models.ForeignKey(Project)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")
        ordering = ("name",)

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.category)


class Repository(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=50)  # should be 'dropbox', 'google_drive', etc
    access_token = models.CharField(max_length=500)  # access token obtained via Oauth/Oauth2
    repo_user_id = models.CharField(max_length=200)
    additional_data = models.CharField(max_length=500, null=True, blank=True)
    ela_directory = models.CharField(max_length=200, null=True, blank=True)  # where to save ela stuff
    ela_directory_link = models.CharField(max_length=200, null=True, blank=True)  # given by project creator
