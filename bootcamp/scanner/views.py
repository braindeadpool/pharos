from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from bootcamp.authentication.models import Profile
from bootcamp.devices.models import Device
from bootcamp.projects.models import Project, Collaborator
from bootcamp.feeds.models import Feed
from bootcamp.feeds.views import FEEDS_NUM_PAGES, feeds


def scan_main(request):
    return render(request, 'scanner/wizard.html')


def scan_device(request, identification):
    device = get_object_or_404(Device, identification=identification)
    request.user = User.objects.get(username='scanner')
    return render(request, 'devices/device.html', {'device': device})


def scan_user(request, identification):
    profile = get_object_or_404(Profile, identification=identification)
    page_user = profile.user
    all_projects = Project.get_published_by_user(page_user)
    return render(request, 'scanner/projects.html', {
        'identification': identification,
        'page_user': page_user,
        'projects': all_projects,
    })


def scan_project(request, identification, project_name):
    project = get_object_or_404(Project, slug=project_name)
    profile = get_object_or_404(Profile, identification=identification)
    page_user = profile.user
    return render(request, 'scanner/samples.html', {
          'identification': identification,
          'page_user': page_user,
          'project': project,
    })
