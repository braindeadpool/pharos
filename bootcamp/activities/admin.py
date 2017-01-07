'''
Created on Jan 6, 2017

@author: Vansh-PC
'''
from django.contrib import admin

from .models import Activity,Notification

admin.site.register(Activity)
admin.site.register(Notification)