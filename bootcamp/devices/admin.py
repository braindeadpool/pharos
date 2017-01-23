'''
Created on Jan 6, 2017

@author: Vansh-PC
'''
from django.contrib import admin

from .models import Device, DeviceComment, Collaborator, Tag

admin.site.register(Device)
admin.site.register(DeviceComment)
admin.site.register(Collaborator)
admin.site.register(Tag)
