'''
Created on Jan 6, 2017

@author: Vansh-PC
'''
from django.contrib import admin

from .models import Question,Answer,Tag

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
