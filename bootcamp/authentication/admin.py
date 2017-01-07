'''
Created on Jan 6, 2017

@author: Vansh-PC
'''
from django.contrib import admin

from .models import Profile,LinkedInProfile

admin.site.register(Profile)
admin.site.register(LinkedInProfile)
