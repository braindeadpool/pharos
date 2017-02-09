from django.conf.urls import url

from bootcamp.samples import views

urlpatterns = [
    url(r'^$', views.samples, name='samples'),
    url(r'^add/$', views.add, name='samples_add'),
    url(r'^preview/$', views.preview, name='samples_preview'),
    url(r'^drafts/$', views.drafts, name='sample_drafts'),
    # url(r'^comment/$', views.comment, name='comment'),
    url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='sample_tag'),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_sample'),
    url(r'^(?P<slug>[-\w]+)/$', views.sample, name='sample'),
]
