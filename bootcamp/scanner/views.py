from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from bootcamp.authentication.models import Profile
from bootcamp.devices.models import Device
from bootcamp.projects.models import Project
from bootcamp.samples.forms import SampleForm
from bootcamp.samples.models import Sample


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
    return render(request, 'scanner/user.html', {
        'identification': identification,
        'page_user': page_user,
        'projects': all_projects,
    })


def scan_sample(request, identification, sample_id=None):
    profile = get_object_or_404(Profile, identification=identification)
    page_user = profile.user
    sample = None
    if request.method == 'POST':
        form = SampleForm(request.POST, user=page_user)
        if form.is_valid():
            sample = Sample()
            sample.create_user = request.user
            sample.title = form.cleaned_data.get('title')
            sample.description = form.cleaned_data.get('description')
            sample.identification = form.cleaned_data.get('identification')

            status = form.cleaned_data.get('status')
            if status in [Sample.PUBLISHED, Sample.DRAFT]:
                sample.status = form.cleaned_data.get('status')
            sample.save()
            tags = form.cleaned_data.get('tags')
            sample.create_tags(tags)

    else:
        samples = Sample.objects.filter(identification=sample_id)
        if len(samples) == 1:
            sample = samples[0]

    if sample:
        # sample exists already, so display it
        return render(request, 'scanner/sample.html', {
            'identification': identification,
            'page_user': page_user,
            'sample': sample,
            'new_sample': False
        })
    else:
        # sample doesn't exist, so fill up form with it
        form = SampleForm(user=page_user)
        return render(request, 'scanner/add_sample.html', {
            'identification': identification,
            'page_user': page_user,
            'sample': sample,
            'form': form,
            'new_sample': True
        })


def scan_project(request, identification, project_name):
    project = get_object_or_404(Project, slug=project_name)
    profile = get_object_or_404(Profile, identification=identification)
    page_user = profile.user

    # setup the form
    if request.method == 'POST':
        form = SampleForm(request.POST, user=page_user)
        if form.is_valid():
            sample = Sample()
            sample.create_user = request.user
            sample.title = form.cleaned_data.get('title')
            sample.description = form.cleaned_data.get('description')

            status = form.cleaned_data.get('status')
            if status in [Sample.PUBLISHED, Sample.DRAFT]:
                sample.status = form.cleaned_data.get('status')
            sample.save()
            tags = form.cleaned_data.get('tags')
            sample.create_tags(tags)

            return redirect('/samples/')
    else:
        form = SampleForm(user=page_user)
    return render(request, 'scanner/samples.html', {
        'identification': identification,
        'page_user': page_user,
        'project': project,
        'form': form
    })
