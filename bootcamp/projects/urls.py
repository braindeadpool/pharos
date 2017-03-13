from django.conf.urls import url

from bootcamp.projects import views

urlpatterns = [
    url(r'^$', views.projects, name='projects'),
    url(r'^connect_repository', views.connect_repository, name='connect_repository'),
    url(r'^access_repository', views.access_repository, name='access_repository'),
    url(r'^dropbox_auth_start', views.dropbox_auth_start, name='dropbox_auth_start'),
    url(r'^dropbox_auth_finish', views.dropbox_auth_finish, name='dropbox_auth_finish'),
    url(r'^search/$', views.search_projects, name='search_projects'),
    url(r'^write/$', views.write, name='write'),
    url(r'^preview/$', views.preview, name='preview'),
    url(r'^drafts/$', views.drafts, name='drafts'),
    url(r'^comment/$', views.comment, name='comment'),
    url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    url(r'^author/(?P<author_name>.+)/$', views.author, name='author'),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_project'),
    url(r'^collaborator_lookup/$', views.collaborator_lookup, name='collaborator_lookup'),
    url(r'^(?P<slug>[-\w]+)/$', views.project, name='project'),
]
