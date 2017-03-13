from django.contrib import admin

from .models import Project, ProjectComment, Tag, Collaborator, Material, Repository

admin.site.register(Project)
admin.site.register(ProjectComment)
admin.site.register(Tag)
admin.site.register(Collaborator)
admin.site.register(Material)
admin.site.register(Repository)
