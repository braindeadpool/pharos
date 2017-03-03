from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.contrib import messages

from PIL import Image

import bootcamp.core.all_users as all_users
import markdown
from bootcamp.devices.forms import DeviceForm
from bootcamp.devices.models import Device, DeviceComment, DeviceImage, Tag, Collaborator
from bootcamp.decorators import ajax_required

PROJECTS_NUM_PAGES = 100


def _devices(request, devices):
    paginator = Paginator(devices, 100)
    page = request.GET.get('page')
    try:
        devices = paginator.page(page)
    except PageNotAnInteger:
        devices = paginator.page(1)
    except EmptyPage:
        devices = paginator.page(paginator.num_pages)
    popular_tags = Tag.get_popular_tags()
    return render(request, 'devices/devices.html', {
        'devices': devices,
        'popular_tags': popular_tags
    })


@login_required
def devices(request):
    all_devices = Device.get_published()
    return _devices(request, all_devices)


@login_required
def devicesByUser(request):
    all_devices = Device.objects.filter(create_user=request.user,
                                          status=Device.PUBLISHED)
    return _devices(request, all_devices)


@login_required
def device(request, slug):
    device = get_object_or_404(Device, slug=slug, status=Device.PUBLISHED)
    device.picture = device.get_picture()
    device.pictures = device.get_pictures()
    return render(request, 'devices/device.html', {'device': device})


@login_required
def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    devices = []
    for tag in tags:
        if tag.device.status == Device.PUBLISHED:
            devices.append(tag.device)
    return _devices(request, devices)


def persist_collaborators(collaborators, proj):
    # collaborators is a list, for each request we need to persist them
    userMap = all_users.getUserDictionary()
    print userMap
    for each in collaborators:
        t, created = Collaborator.objects.get_or_create(device=proj,
                                                        user=userMap[each])


@login_required
def write(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST, request.FILES)
        if form.is_valid():
            device = Device()
            device.create_user = request.user
            device.name = form.cleaned_data.get('name')
            device.description = form.cleaned_data.get('description')
            device.identification = form.cleaned_data.get('identification')
            device.images = form.cleaned_data.get('pictures')

            collaborators = form.cleaned_data.get('collaborators')
            collaborators.append(request.user.username)
            collaborators = set(collaborators)

            status = form.cleaned_data.get('status')
            if status in [Device.PUBLISHED, Device.DRAFT]:
                device.status = form.cleaned_data.get('status')
            device.save()

            # save image
            for each in device.images:
                image = DeviceImage(image=each, device=device)
                image.save()

            persist_collaborators(collaborators, device)
            tags = form.cleaned_data.get('tags')
            device.create_tags(tags)

            return redirect('/devices/')
    else:
        print "rendering init form"
        form = DeviceForm()
    return render(request, 'devices/write.html', {'form': form})


@login_required
def drafts(request):
    drafts = Device.objects.filter(create_user=request.user,
                                    status=Device.DRAFT)
    return render(request, 'devices/drafts.html', {'drafts': drafts})


@login_required
def edit(request, id):
    tags = ''
    if id:
        device = get_object_or_404(Device, pk=id)
        for tag in device.get_tags():
            tags = '{0} {1}'.format(tags, tag.tag)
        tags = tags.strip()
        collaborators = [x.user.username for x in device.get_collaborators()]
    else:
        device = Device(create_user=request.user)

    if request.user.username not in collaborators:
        messages.add_message(request, messages.ERROR,
                             'You are not authorized to edit this Device- ' + device.title + '. Only collaborators can edit their Device')
        return redirect('/devices/')

    if request.POST:
        form = DeviceForm(request.POST, request.FILES, instance=device)
        if form.is_valid():
            form.save()
            device.delete_tags()
            device.delete_collaborators()
            collaborators = form.cleaned_data.get('collaborators')
            tags = form.cleaned_data.get('tags')
            device.images = form.cleaned_data.get('pictures')
            # save images

            for each in device.images:
                image = DeviceImage(image=each, device=device)
                image.save()
            persist_collaborators(collaborators, device)
            device.create_tags(tags)
            return redirect('/devices/')
    else:
        form = DeviceForm(instance=device)
        form.fields['tags'].initial = tags
        form.fields['collaborators'].initial = collaborators

    return render(request, 'devices/edit.html', {'form': form})


@login_required
@ajax_required
def preview(request):
    try:
        if request.method == 'POST':
            description = request.POST.get('description')
            html = 'Nothing to display :('
            if len(description.strip()) > 0:
                html = markdown.markdown(description, safe_mode='escape')
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()

    except Exception:
        return HttpResponseBadRequest()


@login_required
@ajax_required
def comment(request):
    try:
        if request.method == 'POST':
            device_id = request.POST.get('device')
            device = Device.objects.get(pk=device_id)
            comment = request.POST.get('comment')
            comment = comment.strip()
            if len(comment) > 0:
                device_comment = DeviceComment(user=request.user,
                                                 device=device,
                                                 comment=comment)
                device_comment.save()
            html = ''
            for comment in device.get_comments():
                html = '{0}{1}'.format(html, render_to_string(
                    'devices/partial_device_comment.html',
                    {'comment': comment}))

            return HttpResponse(html)

        else:
            return HttpResponseBadRequest()

    except Exception:
        return HttpResponseBadRequest()
