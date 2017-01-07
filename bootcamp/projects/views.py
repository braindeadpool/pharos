from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.contrib import messages

import bootcamp.core.all_users as all_users
import markdown
from bootcamp.projects.forms import ProjectForm
from bootcamp.projects.models import Project, ProjectComment, Tag, Collaborator, Material
from bootcamp.decorators import ajax_required

PROJECTS_NUM_PAGES = 100


def _projects(request, projects):
    paginator = Paginator(projects, 100)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    popular_tags = Tag.get_popular_tags()
    return render(request, 'projects/projects.html', {
        'projects': projects,
        'popular_tags': popular_tags
    })


@login_required
def projects(request):
    all_projects = Project.get_published()
    return _projects(request, all_projects)


@login_required
def projectsByUser(request):
    all_projects = Project.objects.filter(create_user=request.user,
                                    status=Project.PUBLISHED)
    return _projects(request, all_projects)



@login_required
def project(request, slug):
    print "reached here"
    project = get_object_or_404(Project, slug=slug, status=Project.PUBLISHED)
    print "This is the project", project
    return render(request, 'projects/project.html', {'project': project})


@login_required
def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    projects = []
    for tag in tags:
        if tag.project.status == Project.PUBLISHED:
            projects.append(tag.project)
    return _projects(request, projects)


def persist_collaborators(collaborators, proj):
    #collaborators is a list, for each request we need to persist them
    userMap = all_users.getUserDictionary()
    for each in collaborators:
        t, created = Collaborator.objects.get_or_create(project = proj,
                                                        user = userMap[each])
        
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
            
            print "The collaborators are: "            
            print collaborators
            
            status = form.cleaned_data.get('status')
            if status in [Project.PUBLISHED, Project.DRAFT]:
                project.status = form.cleaned_data.get('status')
            project.save()
            persist_collaborators(collaborators, project)
            tags = form.cleaned_data.get('tags')
            project.create_tags(tags)
            
            #get materials
            material =  request.POST.getlist('material[]')
            category = request.POST.getlist('category[]')
            for i in range(len(material)):
                toInsert = Material()
                toInsert.name = material[i]
                toInsert.category = category[i]
                toInsert.project = project
                toInsert.save()
            
            return redirect('/projects/')
    else:
        print "rendering init form"
        form = ProjectForm()
    return render(request, 'projects/write.html', {'form': form})


@login_required
def drafts(request):
    drafts = Project.objects.filter(create_user=request.user,
                                    status=Project.DRAFT)
    return render(request, 'projects/drafts.html', {'drafts': drafts})


@login_required
def edit(request, id):
    print "Ok reached here"
    tags = ''
    if id:
        project = get_object_or_404(Project, pk=id)
        for tag in project.get_tags():
            tags = '{0} {1}'.format(tags, tag.tag)
        tags = tags.strip()
        collaborators = [x.user.username for x in  project.get_collaborators()]
        print collaborators
    else:
        project = Project(create_user=request.user)

    if request.user.username not in collaborators:
        messages.add_message(request, messages.ERROR,
                                 'You are not authorized to edit this Project- ' + project.title + '. Only collaborators can edit their Project')
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
        print form.fields['collaborators']
        print form
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
