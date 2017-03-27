from django.conf.urls import url

from bootcamp.scanner import views

urlpatterns = [
    url(r'^$', views.scan_main, name='scan_main'),
    url(r'^device/(?P<identification>\w+)/$', views.scan_device, name='scan_device'),
    url(r'^project/(?P<identification>\w+)/(?P<project_name>[-\w]+)/$', views.scan_project, name='scan_project'),
    url(r'^user/(?P<identification>\w+)/$', views.scan_user, name='scan_user'),
]
