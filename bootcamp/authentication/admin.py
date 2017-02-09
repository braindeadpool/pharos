'''
Created on Jan 6, 2017

@author: Vansh-PC
'''
from django.contrib import admin

from .models import Profile, LinkedInProfile, Link

admin.site.register(Profile)
admin.site.register(LinkedInProfile)
admin.site.register(Link)
