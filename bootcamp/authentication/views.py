from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from bootcamp.authentication.forms import SignUpForm
from bootcamp.feeds.models import Feed


def signup(request):
    # default external links to be added to profiles - stored as label( or alt name) and logo file name in static/img/
    default_links = [['LinkedIn', 'linkedin-logo.png'],
                     ['Google Scholar', 'google-scholar-logo.png'],
                     ['Github', 'github-logo.png'],
                     ['Flickr', 'flickr-logo.png'],
                     ['ResearchGate', 'researchgate-logo.png'],
                     ]
    datalists = {}
    active_users = [x for x in User.objects.filter(is_active=True)]
    datalists['institution'] = sorted(set([x.profile.institution for x in active_users]))
    if request.method == 'POST':
        form = SignUpForm(request.POST, datalists=datalists)
        if not form.is_valid():
            return render(request, 'authentication/signup.html',
                          {'form': form})
        else:
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            identification = form.cleaned_data.get('identification')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            role = form.cleaned_data.get('role')
            job_title = form.cleaned_data.get('job_title')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            country = form.cleaned_data.get('country')
            institution = form.cleaned_data.get('institution')
            web_page = form.cleaned_data.get('web_page')
            bio = form.cleaned_data.get('bio')

            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            # user.profile.role = role
            user.profile.job_title = job_title
            user.profile.state = state
            user.profile.country = country
            user.profile.institution = institution
            user.profile.web_page = web_page
            user.profile.bio = bio
            user.profile.city = city
            user.save()
            #             if role == 'Lab Manager':
            #                 names =  request.POST.getlist('field_stu[]')
            #                 insts =  request.POST.getlist('university[]')
            #                 rooms =  request.POST.getlist('room[]')
            #                 cities =  request.POST.getlist('city[]')
            #                 states =  request.POST.getlist('state[]')
            #                 countries =  request.POST.getlist('country[]')
            #                 device_names = request.POST.getlist('device_name[]')
            #                 descriptions = request.POST.getlist('description[]')
            #
            #                 for i in range(len(names)):
            #                     Project = Lab()
            #                     Project.manager = user
            #                     Project.name = names[i]
            #                     Project.institution = insts[i]
            #                     Project.building = rooms[i]
            #                     Project.city = cities[i]
            #                     Project.state = states[i]
            #                     Project.country = countries[i]
            #                     Project.save()
            #                     device = Device()
            #                     device.manager = Project.manager
            #                     device.name = device_names[i]
            #                     device.desciption = descriptions[i]
            #                     device.requestor = Project.manager.username
            #                     device.Project = Project
            #                     device.save()
            #


            login(request, user)
            welcome_post = '{0} has joined the network.'.format(user.username,
                                                                user.username)
            feed = Feed(user=user, post=welcome_post)
            feed.save()

            return redirect('/connect_repositories/')

    else:
        return render(request, 'authentication/signup.html',
                      {'form': SignUpForm(datalists=datalists),
                       'default_links': default_links,})
