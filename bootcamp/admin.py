from django.contrib import admin

from .activities.models import Activity,Notification
from bootcamp.authentication.models import Profile,LinkedInProfile,Lab,Device
from bootcamp.authentication.models import Profile,LinkedInProfile,Lab,Device
from bootcamp.feeds.models import Feed
from bootcamp.messenger.models import Message
from bootcamp.projects.models import Project,Tag,ProjectComment,Collaborator, Material
import bootcamp.questions.models #import Question,Tag,Answer

admin.site.register(Activity)
admin.site.register(Notification)

