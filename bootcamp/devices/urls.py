from django.conf.urls import url

from bootcamp.devices import views

urlpatterns = [
    url(r'^$', views.devices, name='devices'),
    url(r'^write/$', views.write, name='device_write'),
    url(r'^preview/$', views.preview, name='device_preview'),
    url(r'^drafts/$', views.drafts, name='device_drafts'),
    url(r'^comment/$', views.comment, name='device_comment'),
    url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='device_tag'),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_device'),
    url(r'^(?P<slug>[-\w]+)/$', views.device, name='device'),
]
