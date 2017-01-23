# from __future__ import unicode_literals
#
# from datetime import datetime
#
# from django.contrib.auth.models import User
# from django.db import models
# from django.template.defaultfilters import slugify
# from django.utils.encoding import python_2_unicode_compatible
# from django.utils.translation import ugettext_lazy as _
#
# from bootcamp.samples.models import Sample
# from bootcamp.devices.models import Device
#
# import markdown
#
#
# @python_2_unicode_compatible
# class Scanner(models.Model):
#     slug = models.SlugField(max_length=255, null=True, blank=True)
#
#     class Meta:
#         verbose_name = _("Scanner")
#         verbose_name_plural = _("Scanners")
#
#     def __str__(self):
#         return "Scanner"
#
#     def save(self, *args, **kwargs):
#         if not self.pk:
#             super(Scanner, self).save(*args, **kwargs)
#         else:
#             self.update_date = datetime.now()
#         if not self.slug:
#             slug_str = "%s %s" % (self.pk, self.title.lower())
#             self.slug = slugify(slug_str)
#         super(Scanner, self).save(*args, **kwargs)
#
#     def get_description_as_markdown(self):
#         return markdown.markdown(self.description, safe_mode='escape')
#
#
#
# class Device(models.Model):
#     scanner = models.ForeignKey(Scanner)
#     identification = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#
#     class Meta:
#         verbose_name = _("Device")
#         verbose_name_plural = _("Devices")
#         ordering = ("name",)
#
#     def __str__(self):
#         return '{0} - {1}'.format(self.name, self.location)
#
#
# class Sample(models.Model):
#     scanner = models.ForeignKey(Scanner)
#     sample = models.ForeignKey(samples_models.Sample)
#     date = models.DateTimeField(auto_now_add=True)
#     name = models.CharField(max_length=255)
#     category = models.CharField(max_length=255)
#
#     class Meta:
#         verbose_name = _("Sample")
#         verbose_name_plural = _("Samples")
#         ordering = ("name",)
#
#     def __str__(self):
#         return '{0} - {1}'.format(self.name, self.category)
