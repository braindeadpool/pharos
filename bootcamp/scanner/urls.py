from django.conf.urls import url

from bootcamp.scanner import views

urlpatterns = [
    url(r'^$', views.scan_main, name='scan_main'),
    url(r'^device/(?P<identification>\w+)/$', views.scan_device, name='scan_device'),
    url(r'^sample/(?P<identification>\w+)/(?P<sample_id>[-\w]+)/$', views.scan_sample, name='scan_sample'),
    url(r'^sample/(?P<identification>\w+)/$', views.scan_sample, name='scan_sample'),
    url(r'^user/(?P<identification>\w+)/$', views.scan_user, name='scan_user'),
]
