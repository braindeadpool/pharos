from django.conf.urls import url

from bootcamp.devices import views

urlpatterns = [
    url(r'^$', views.devices, name='devices'),
    url(r'^write/$', views.write, name='write'),
    url(r'^preview/$', views.preview, name='preview'),
    url(r'^drafts/$', views.drafts, name='drafts'),
    url(r'^comment/$', views.comment, name='comment'),
    url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_device'),
    url(r'^(?P<slug>[-\w]+)/$', views.device, name='device'),
]
