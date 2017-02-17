from django.conf.urls import url

from bootcamp.projects import views

urlpatterns = [
    url(r'^$', views.projects, name='projects'),
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
