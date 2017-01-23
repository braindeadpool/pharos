from django.conf.urls import url

from bootcamp.labs import views

urlpatterns = [
    url(r'^$', views.labs, name='labs'),
    url(r'^write/$', views.write, name='write'),
    url(r'^preview/$', views.preview, name='preview'),
    url(r'^drafts/$', views.drafts, name='drafts'),
    url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_lab'),
    url(r'^(?P<slug>[-\w]+)/$', views.lab, name='lab'),
]
