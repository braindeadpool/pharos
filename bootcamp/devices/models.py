from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import os

import markdown


@python_2_unicode_compatible
class Device(models.Model):
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
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True,
                                    related_name="+")

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
        ordering = ("-create_date",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Device, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s %s" % (self.pk, self.name.lower())
            self.slug = slugify(slug_str)
        super(Device, self).save(*args, **kwargs)

    def get_description_as_markdown(self):
        return markdown.markdown(self.description, safe_mode='escape')

    @staticmethod
    def get_published():
        devices = Device.objects.filter(status=Device.PUBLISHED)
        return devices

    @staticmethod
    def get_published_by_user(user):
        devices = Device.objects.filter(status=Device.PUBLISHED, create_user=user)
        return devices

    def get_picture(self):
        no_picture = settings.MEDIA_URL + '/device_pictures/default.png'
        try:
            filename = settings.MEDIA_ROOT + '/device_pictures/' + self.identification + '.jpg'
            picture_url = settings.MEDIA_URL + 'device_pictures/' + self.identification + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                return no_picture

        except Exception as e:
            print e
            return no_picture

    def get_pictures(self):
        pictures = DeviceImage.objects.filter(device=self)
        print pictures
        if len(pictures) == 0:
            return [{'id': 0, 'image': 'device_pictures/default.png'}]
        else:
            return pictures

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                t, created = Tag.objects.get_or_create(tag=tag.lower(),
                                                       device=self)

    def get_tags(self):
        return Tag.objects.filter(device=self)

    def delete_tags(self):
        Tag.objects.filter(device=self).delete()

    def delete_pictures(self):
        DeviceImage.objects.filter(device=self).delete()

    def delete_collaborators(self):
        Collaborator.objects.filter(device=self).delete()

    def get_collaborators(self):
        return Collaborator.objects.filter(device=self)


    def get_collaborators_comma_delimited(self):
        all = Collaborator.objects.filter(device=self)
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
        return DeviceComment.objects.filter(device=self)


@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=50)
    device = models.ForeignKey(Device)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        unique_together = (('tag', 'device'),)
        index_together = [['tag', 'device'], ]

    def __str__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        tags = Tag.objects.all()
        count = {}
        for tag in tags:
            if tag.device.location == Device.PUBLISHED:
                if tag.tag in count:
                    count[tag.tag] = count[tag.tag] + 1
                else:
                    count[tag.tag] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]


@python_2_unicode_compatible
class DeviceComment(models.Model):
    device = models.ForeignKey(Device)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _("Device Comment")
        verbose_name_plural = _("Device Comments")
        ordering = ("date",)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.device.name)


@python_2_unicode_compatible
class DeviceImage(models.Model):
    image = models.ImageField(upload_to='device_pictures/')
    device = models.ForeignKey(Device)
    date = models.DateTimeField(auto_now_add=True)
    alt_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Device Image")
        verbose_name_plural = _("Device Images")
        ordering = ("date",)

    def __str__(self):
        return '{}_image_{}'.format(self.device.name, self.id)


@python_2_unicode_compatible
class Collaborator(models.Model):
    device = models.ForeignKey(Device)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="device_collaborator")

    @staticmethod
    def get_published_by_user(userid):
        objs = Collaborator.objects.filter(user=userid)
        devices = [x.device for x in objs if (x.device.location == Device.PUBLISHED)]
        return devices

    class Meta:
        verbose_name = _("Collaborator")
        verbose_name_plural = _("Collaborators")
        ordering = ("user",)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.device.name)

