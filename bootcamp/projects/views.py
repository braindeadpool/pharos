from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

import bootcamp.core.all_users as all_users
import markdown
from bootcamp.projects.forms import ProjectForm, SearchForm
from bootcamp.projects.models import Project, ProjectComment, Tag, Collaborator, Material, Device, Sample
from bootcamp.decorators import ajax_required
import simplejson

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
            Q(create_user__first_name__icontains=author) | Q(create_user__last_name__icontains=author)) & Q(tag__tag__icontains=tag_values)).distinct()
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
    return render(request, 'projects/project.html', {'project': project})


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
                print "Inserting of {} failed".format(material)
                print "Inserting of {} failed".format(category)

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
                    toInsert.save()
            except:
                print "Inserting of {} failed".format(device)

            return redirect('/projects/')
    else:
        print
        "rendering init form"
        form = ProjectForm()
    return render(request, 'projects/write.html', {'form': form})


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
