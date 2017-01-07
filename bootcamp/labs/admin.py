'''
Created on Jan 6, 2017

@author: Vansh-PC
'''
from django.contrib import admin

from .models import Lab, Tag, Device

admin.site.register(Lab)
admin.site.register(Tag)
admin.site.register(Device)
