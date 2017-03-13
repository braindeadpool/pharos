from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

import bootcamp.core.all_users as all_users
import markdown
from bootcamp.projects.forms import ProjectForm, SearchForm
from bootcamp.projects.models import Project, ProjectComment, Tag, Collaborator, Material, Device, Repository
from bootcamp.decorators import ajax_required

from bootcamp.settings import DROPBOX_CONSUMER_KEY, DROPBOX_CONSUMER_SECRET, BASE_URL, DEFAULT_REPOS
from dropbox import DropboxOAuth2Flow
import dropbox

PROJECTS_NUM_PAGES = 100


def _projects(request, projects, form=SearchForm()):
    popular_authors = Project.get_popular_authors(projects)
    popular_tags = Tag.get_popular_tags(projects)
    paginator = Paginator(projects, 100)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'projects/projects.html', {
        'projects': projects,
        'popular_tags': popular_tags,
        'popular_authors': popular_authors,
        'form': form
    })


@login_required
def projects(request):
    all_projects = Project.get_published()
    for project in all_projects:
        collaborators = [x.user for x in project.get_collaborators()]
        project.collaborators = collaborators
        if request.user == project.create_user or request.user in collaborators:
            project.editable = True
        else:
            project.editable = False
    return _projects(request, all_projects)


@login_required
def search_projects(request):
    if request.method == "GET" and len(request.GET) > 0:
        form = SearchForm(request.GET)
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')
        daterange = request.GET.get('daterange', '')
        tag_values = request.GET.get('tags', '')
        results = Project.objects.filter(
            Q(title__icontains=title) & (
                Q(create_user__first_name__icontains=author) | Q(create_user__last_name__icontains=author)) & Q(
                tag__tag__icontains=tag_values)).distinct()
        return _projects(request, results, form)
    else:
        return render(request, 'projects/search.html', {'form': SearchForm()})


@login_required
def projectsByUser(request):
    all_projects = Project.objects.filter(create_user=request.user,
                                          status=Project.PUBLISHED)
    return _projects(request, all_projects)


@login_required
def project(request, slug):
    print
    "reached here"
    project = get_object_or_404(Project, slug=slug, status=Project.PUBLISHED)
    collaborators = [x.user for x in project.get_collaborators()]
    if request.user == project.create_user or request.user in collaborators:
        project.editable = True
    else:
        project.editable = False
    repository = Repository.objects.filter(project=project)
    repo = None
    if len(repository) ==1:
        repo = repository[0]
        repo.logo = DEFAULT_REPOS[repository[0].name][1]
    else:
        print "Invalid number of repositories found {}".format(repository)

    return render(request, 'projects/project.html', {'project': project, 'repository':repo})


@login_required
def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    projects = []
    for tag in tags:
        if tag.project.status == Project.PUBLISHED:
            projects.append(tag.project)
    return _projects(request, projects)


@login_required
def author(request, author_name):
    all_projects = Project.objects.filter(create_user__username=author_name)
    return _projects(request, all_projects)


def persist_collaborators(collaborators, proj):
    # collaborators is a list, for each request we need to persist them
    userMap = all_users.getUserDictionary()
    print
    userMap
    for each in collaborators:
        t, created = Collaborator.objects.get_or_create(project=proj,
                                                        user=userMap[each])


def collaborator_lookup(request):
    # Default return list
    results = []
    if request.method == "GET":
        if 'term' in request.GET.keys():
            value = request.GET['term']
            model_results = User.objects.filter(
                Q(username__icontains=value) | Q(first_name__icontains=value) | Q(last_name__icontains=value))
            results = [
                {'id': x.id, 'label': x.first_name + ' ' + x.last_name, 'value': x.first_name + ' ' + x.last_name,
                 'username': x.username} for x in model_results]
    return JsonResponse(results, safe=False)


@login_required
def write(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project()
            project.create_user = request.user
            project.title = form.cleaned_data.get('title')
            project.description = form.cleaned_data.get('description')
            collaborators = form.cleaned_data.get('collaborators')
            collaborators.append(request.user.username)
            collaborators = set(collaborators)

            status = form.cleaned_data.get('status')
            if status in [Project.PUBLISHED, Project.DRAFT]:
                project.status = form.cleaned_data.get('status')
            project.save()
            persist_collaborators(collaborators, project)
            tags = form.cleaned_data.get('tags')
            project.create_tags(tags)

            # get materials and devices
            material = request.POST.getlist('material[]')
            category = request.POST.getlist('category[]')
            try:
                for i in range(len(material)):
                    toInsert = Material()
                    toInsert.name = material[i]
                    toInsert.category = category[i]
                    toInsert.project = project
                    toInsert.save()
            except:
                print
                "Inserting of {} failed".format(material)
                print
                "Inserting of {} failed".format(category)

            device = request.POST.getlist('device[]')
            device_id = request.POST.getlist('device_identification[]')
            device_location = request.POST.getlist('device_location[]')
            try:
                for i in range(len(device)):
                    toInsert = Device()
                    toInsert.name = device[i]
                    toInsert.identification = device_id[i]
                    toInsert.location = device_location[i]
                    toInsert.project = project
                    toInsert.create_user = request.user
                    toInsert.save()
            except:
                print
                "Inserting of {} failed".format(device)

            repo = request.session['repo']
            print repo
            access_token = request.POST.get('access_token')
            ela_directory_link = request.POST.get('ela_directory')

            print access_token, ela_directory_link

            # validate the token and the directory link
            if access_token == repo['access_token']:
                print "Access token matches - no hijacking!"
            else:
                print "Access token mismatch - server has {} while form gave {}".format(repo['access_token'], access_token)
                raise AssertionError

            dbx = dropbox.Dropbox(access_token)
            ela_directory = '/'
            try:
                metadata = dbx.sharing_get_shared_link_metadata(ela_directory_link)
                print metadata
                # add checks to see if its accessible here
                ela_directory = metadata.path_lower
            except Exception, e:
                print e
                raise

            repoInstance = Repository()
            repoInstance.access_token = access_token
            repoInstance.project = project
            repoInstance.repo_user_id = repo['repo_user_id']
            repoInstance.additional_data = repo['additional_data']
            repoInstance.name = repo['name']
            repo.ela_directory_link = ela_directory_link
            repoInstance.ela_directory = ela_directory
            repoInstance.save()

            print "repository link saved for this project"

            return redirect('/projects/')
    else:
        print
        "rendering init form"
        form = ProjectForm()
    return render(request, 'projects/write.html', {'form': form, 'repos': DEFAULT_REPOS})


@login_required
def drafts(request):
    drafts = Project.objects.filter(create_user=request.user,
                                    status=Project.DRAFT)
    return render(request, 'projects/drafts.html', {'drafts': drafts})


@login_required
def edit(request, id):
    print
    "Ok reached here"
    tags = ''
    if id:
        project = get_object_or_404(Project, pk=id)
        for tag in project.get_tags():
            tags = '{0} {1}'.format(tags, tag.tag)
        tags = tags.strip()
        collaborators = [x.user.username for x in project.get_collaborators()]
        print
        collaborators
    else:
        project = Project(create_user=request.user)

    if request.user.username not in collaborators and request.user.username != project.create_user.username:
        messages.add_message(request, messages.ERROR,
                             'You are not authorized to edit "' + project.title + '". Only collaborators and creator can edit their project')
        return redirect('/projects/')

    if request.POST:
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            project.delete_tags()
            project.delete_collaborators()
            collaborators = form.cleaned_data.get('collaborators')
            tags = form.cleaned_data.get('tags')
            persist_collaborators(collaborators, project)
            project.create_tags(tags)
            return redirect('/projects/')
    else:
        form = ProjectForm(instance=project)
        form.fields['tags'].initial = tags
        form.fields['collaborators'].initial = collaborators
        print
        form.fields['collaborators']
        print
        form
    return render(request, 'projects/edit.html', {'form': form})


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
            project_id = request.POST.get('project')
            project = Project.objects.get(pk=project_id)
            comment = request.POST.get('comment')
            comment = comment.strip()
            if len(comment) > 0:
                project_comment = ProjectComment(user=request.user,
                                                 project=project,
                                                 comment=comment)
                project_comment.save()
            html = ''
            for comment in project.get_comments():
                html = '{0}{1}'.format(html, render_to_string(
                    'projects/partial_project_comment.html',
                    {'comment': comment}))

            return HttpResponse(html)

        else:
            return HttpResponseBadRequest()

    except Exception:
        return HttpResponseBadRequest()


### -------- REPOSITORIES ------------- ###


@login_required
def connect_repository(request):
    return render(request, 'projects/connect_repository.html',
                  {'repos': DEFAULT_REPOS})


@login_required
def access_repository(request, repo=None):
    if repo is None:
        repo = Repository.objects.get(user=request.user)
    account_linked = repo is not None
    if account_linked:
        # setup client
        # dbx = dropbox.Dropbox(repo.access_token)
        ela_directory = '/'  # defaults to root directory
        # check for ela directory
        try:
            if repo.ela_directory is not None:
                ela_directory = repo.ela_directory
        except:
            pass

        # tree_view = list_folder(dbx, ela_directory, recursive=True)
        # print tree_view
        # tree_view = json.dumps(tree_view)
        return render(request, 'projects/dropbox.html', {
            'account_linked': account_linked,
            'repo': repo,
            'ela_directory': ela_directory,
            # 'tree_view': tree_view
        })
    else:
        return render(request, 'projects/dropbox.html', {'account_linked': account_linked})


def get_dropbox_auth_flow(web_app_session):
    redirect_uri = BASE_URL + "/projects/dropbox_auth_finish"
    return DropboxOAuth2Flow(DROPBOX_CONSUMER_KEY, DROPBOX_CONSUMER_SECRET, redirect_uri, web_app_session,
                             "dropbox-auth-csrf-token")


# URL handler for /dropbox-auth-start
def dropbox_auth_start(request):
    # repo = None
    # try:
    #     repo = Repository.objects.filter(project=project)
    # except Repository.DoesNotExist:
    #     repo = None
    # account_linked = repo is not None
    # if account_linked:
    #     return access_dropbox(request, repo)
    authorize_url = get_dropbox_auth_flow(request.session).start()
    print
    "authorize URL = {}".format(authorize_url)
    return HttpResponseRedirect(authorize_url)


# URL handler for /dropbox-auth-finish
def dropbox_auth_finish(request):
    try:
        try:
            if request.session["dropbox-auth-csrf-token"] is None or request.session["dropbox-auth-csrf-token"] == "":
                raise Exception("Problem with csrf")
        except Exception, e:
            # Get it from the parameter and add it to the session.
            csrf = request.GET.get("state")
            request.session["dropbox-auth-csrf-token"] = csrf
        oauth_result = get_dropbox_auth_flow(request.session).finish(request.GET)
        print
        oauth_result
        access_token = "None"
        user_id = "None"
        url_state = "None"
        account_id = "None"
        additional_data = "None, None"
        try:
            access_token = oauth_result.access_token
            user_id = oauth_result.user_id
            url_state = oauth_result.url_state
            account_id = oauth_result.account_id
            additional_data = "{}, {}".format(account_id + url_state)
        except Exception, e:
            print
            e

        dropbox_repo = {}
        dropbox_repo['name'] = 'dropbox'
        dropbox_repo['project'] = None
        dropbox_repo['access_token'] = access_token
        dropbox_repo['repo_user_id'] = user_id
        dropbox_repo['additional_data'] = additional_data
        request.session['repo'] = dropbox_repo
        print "Dropbox info saved in session as {}".format(dropbox_repo)

    except Exception, e:
        raise e
    return render(request, 'projects/repo_connected.html',
                  {'repos': DEFAULT_REPOS,
                   'repo': dropbox_repo})
