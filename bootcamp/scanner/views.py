from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from bootcamp.authentication.models import Profile
from bootcamp.devices.models import Device
from bootcamp.projects.models import Project, Collaborator
from bootcamp.feeds.models import Feed
from bootcamp.feeds.views import FEEDS_NUM_PAGES, feeds


def scan_device(request, identification):
    device = get_object_or_404(Device, identification=identification)
    request.user = User.objects.get(username='scanner')
    return render(request, 'devices/device.html', {'device': device})


def scan_user(request, identification):
    profile = get_object_or_404(Profile, identification=identification)
    page_user = profile.user
    all_feeds = Feed.get_feeds().filter(user=page_user)
    all_projects = Collaborator.get_published_by_user(page_user)
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    feeds = paginator.page(1)
    from_feed = -1
    if feeds:
        from_feed = feeds[0].id
    return render(request, 'core/profile.html', {
        'page_user': page_user,
        'feeds': feeds,
        'from_feed': from_feed,
        'page': 1,
        'projects': all_projects,
    })
