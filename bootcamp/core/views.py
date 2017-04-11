from django.conf import settings as django_settings

from django.contrib.auth import update_session_auth_hash
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render

from bootcamp.core.forms import ChangePasswordForm, ProfileForm
from bootcamp.feeds.models import Feed
from bootcamp.projects.models import Project, Collaborator
from bootcamp.devices.models import Device
from bootcamp.feeds.views import FEEDS_NUM_PAGES, feeds
from bootcamp.authentication.models import LinkedInProfile
from bootcamp.messenger.models import Message
from django.contrib import messages
from PIL import Image

import oauth2 as oauth
import urllib2

from linkedin import linkedin

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from __builtin__ import True

import webbrowser
import os

consumer = oauth.Consumer(settings.LINKEDIN_TOKEN, settings.LINKEDIN_SECRET)
client = oauth.Client(consumer)

request_token_url = 'https://www.linkedin.com/uas/oauth2/authorization'
access_token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'
authenticate_url = 'http://localhost:8000/add_linkedIn.html'

API_KEY = '78pxbqt7x3s1jx'
API_SECRET = 'Yht3OP3IrIBMoZKL'
RETURN_URL = 'http://localhost:8000/add_linkedIn'
perms = ['r_emailaddress', 'r_basicprofile', 'rw_company_admin']

redirect_uri = urllib2.quote('http://localhost:8000/add_linkedIn')
codeURL = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78pxbqt7x3s1jx&redirect_uri=http://localhost:8000/signup/&scope=r_basicprofile"


def home(request):
    if request.user.is_authenticated():
        return redirect('/{}'.format(request.user))
    else:
        return render(request, 'core/cover.html')


@login_required
def network(request):
    users_list = User.objects.filter(is_active=True).order_by('username')
    paginator = Paginator(users_list, 100)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'core/network.html', {'users': users})


@login_required
def quickMessage(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        print
        "from", from_user
        print
        "to", to_user_username
        try:
            to_user = User.objects.get(username=to_user_username)

        except Exception:
            try:
                to_user_username = to_user_username[
                                   to_user_username.rfind('(') + 1:len(to_user_username) - 1]
                to_user = User.objects.get(username=to_user_username)

            except Exception:
                messages.add_message(request, messages.ERROR,
                                     'User ' + to_user_username + " could not be found on the system, fatal error. Please contact the Project manager")
                return network(request)

        message = request.POST.get('message')
        if len(message.strip()) == 0:
            messages.add_message(request, messages.ERROR,
                                 "Cannot send an empty message")
            return network(request)

        if from_user != to_user:
            Message.send_message(from_user, to_user, message)
        messages.add_message(request, messages.SUCCESS,
                             'Your message has been sent')
        return network(request)

    else:
        return network(request)


@login_required
def linkedinRedirection(request):
    print
    "I was here!!!"
    authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, perms)
    code = request.GET.get('code')
    authentication.authorization_code = code
    at = authentication.get_access_token()
    print
    at
    application = linkedin.LinkedInApplication(token=at[0])
    profile = application.get_profile(
        selectors=['id', 'first-name', 'siteStandardProfileRequest', 'last-name', 'location', 'distance',
                   'num-connections', 'skills', 'educations'])
    print
    profile
    #     # Step 3. Lookup the user or create them if they don't exist.
    #     #firstname = profile['firstName']
    #     #lastname = profile['lastName']
    #     identifier = profile['id']
    print
    request.user
    page_user = get_object_or_404(User, username=request.user)
    print
    page_user
    # user = get_object_or_404(User, username=request.user)
    identifier = profile['siteStandardProfileRequest']['url']
    print
    identifier
    LinkedInProfile.objects.get_or_create(identifier=identifier,
                                          user=page_user)
    page_user.profile.isLinkedinPresent = True
    page_user.profile.linkedin_url = identifier
    page_user.save()
    return render(request, 'core/add_linkedIn.html')


@login_required
def addLinkedInProfile(request, username):
    print
    "Started to add Linkedin profile"
    authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, ['r_basicprofile'])
    webbrowser.open(authentication.authorization_url)
    return HttpResponseRedirect(authentication.authorization_url)


@login_required
def profile(request, username):
    page_user = get_object_or_404(User, username=username)
    print
    type(page_user)
    all_feeds = Feed.get_feeds().filter(user=page_user)
    # collaborated_projects = Collaborator.get_published_by_user(page_user)
    collaborated_projects = Project.get_collaborated_by_user(page_user)
    all_projects = Project.get_published_by_user(page_user)
    all_devices = Device.get_published_by_user(page_user)

    collaborators = []
    for project in all_projects:
        collaborators = [x.user for x in project.get_collaborators()]
        if request.user == page_user or request.user in collaborators:
            project.editable = True
        else:
            project.editable = False
    for project in collaborated_projects:
        collaborators += [x.user for x in project.get_collaborators()]

    all_collaborators = []
    for x in collaborators:
        if x != page_user:
            all_collaborators.append(x)

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
        'devices': all_devices,
        'collaborators': all_collaborators,
        'show_chat': page_user == request.user,
    })


@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.email = form.cleaned_data.get('email')
            user.profile.web_page = form.cleaned_data.get('web_page')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.state = form.cleaned_data.get('state')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.institution = form.cleaned_data.get('institution')
            user.profile.bio = form.cleaned_data.get('bio')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')

    else:
        form = ProfileForm(instance=user, initial={
            'job_title': user.profile.job_title,
            'web_page': user.profile.web_page,
            'city': user.profile.city,
            'state': user.profile.state,
            'country': user.profile.country,
            'institution': user.profile.institution,
            'bio': user.profile.bio,
        })

    return render(request, 'core/settings.html', {'form': form})


@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True

    except Exception:
        pass

    return render(request, 'core/picture.html',
                  {'uploaded_picture': uploaded_picture})


@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Your password was successfully changed.')
            return redirect('password')

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'core/password.html', {'form': form})


@login_required
def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('/settings/picture/?upload_picture=uploaded')

    except Exception as e:
        print(e)
        return redirect('/settings/picture/')


@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + \
                       request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + \
                   request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w + x, h + y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)

    except Exception:
        pass

    return redirect('/settings/picture/')
