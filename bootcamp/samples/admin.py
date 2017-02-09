'''
Created on Jan 6, 2017

@author: Vansh-PC
'''
from django.contrib import admin

from .models import Sample, SampleComment, Tag

admin.site.register(Sample)
admin.site.register(SampleComment)
admin.site.register(Tag)
