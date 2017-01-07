'''
Created on Jan 6, 2017

@author: Vansh-PC
'''
from django.contrib import admin

from .models import Project,ProjectComment,Tag,Collaborator, Material

admin.site.register(Project)
admin.site.register(ProjectComment)
admin.site.register(Tag)
admin.site.register(Collaborator)
admin.site.register(Material)