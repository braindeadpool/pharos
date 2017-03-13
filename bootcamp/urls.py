from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from bootcamp.activities import views as activities_views
from bootcamp.authentication import views as bootcamp_auth_views
from bootcamp.core import views as core_views
from bootcamp.search import views as search_views

from django.contrib import admin
from filebrowser.sites import site


urlpatterns = [
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    url(r'^login', auth_views.login, {'template_name': 'core/cover.html'},
        name='login'),
    # url(r'^login/$', linkedin_views.oauth_login, name='login'),
    url(r'^add_linkedIn', core_views.linkedinRedirection, name='linkedin'),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', bootcamp_auth_views.signup, name='signup'),
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/picture/$', core_views.picture, name='picture'),
    url(r'^settings/upload_picture/$', core_views.upload_picture,
        name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', core_views.save_uploaded_picture,
        name='save_uploaded_picture'),
    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^network/$', core_views.network, name='network'),
    url(r'^quickMessage/$', core_views.quickMessage, name='quickMessage'),
    url(r'^feeds/', include('bootcamp.feeds.urls')),
    url(r'^questions/', include('bootcamp.questions.urls')),
    url(r'^projects/', include('bootcamp.projects.urls')),
    url(r'^devices/', include('bootcamp.devices.urls')),
    url(r'^scan/', include('bootcamp.scanner.urls')),
    url(r'^samples/', include('bootcamp.samples.urls')),
    # url(r'^labs/', include('bootcamp.labs.urls')),
    url(r'^messages/', include('bootcamp.messenger.urls')),
    url(r'^notifications/$', activities_views.notifications,
        name='notifications'),
    url(r'^notifications/last/$', activities_views.last_notifications,
        name='last_notifications'),
    url(r'^notifications/check/$', activities_views.check_notifications,
        name='check_notifications'),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^(?P<username>[^/]+)/$', core_views.profile, name='profile'),
    url(r'^(?P<username>[^/]+)/add_linkedin/$', core_views.addLinkedInProfile, name='add_linkedin'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
