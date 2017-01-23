from django.conf.urls import url

from bootcamp.scanner import views

urlpatterns = [
    url(r'^device/(?P<identification>\w+)/$', views.scan_device, name='scan_device'),
    url(r'^user/(?P<identification>\w+)/$', views.scan_user, name='scan_user    '),
]
