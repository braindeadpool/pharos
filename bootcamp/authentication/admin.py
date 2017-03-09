from django.contrib import admin
from .models import Profile, LinkedInProfile, Link, Repository

admin.site.register(Profile)
admin.site.register(LinkedInProfile)
admin.site.register(Link)
admin.site.register(Repository)
