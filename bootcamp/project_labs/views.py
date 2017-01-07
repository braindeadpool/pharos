from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.contrib import messages

import bootcamp.core.all_users as all_users
import markdown
from bootcamp.project_labs.forms import LabForm
from bootcamp.project_labs.models import Lab, Tag
from bootcamp.decorators import ajax_required

LABS_NUM_PAGES = 100


def _labs(request, labs):
    paginator = Paginator(labs, 100)
    page = request.GET.get('page')
    try:
        labs = paginator.page(page)
    except PageNotAnInteger:
        labs = paginator.page(1)
    except EmptyPage:
        labs = paginator.page(paginator.num_pages)
    popular_tags = Tag.get_popular_tags()
    return render(request, 'labs/labs.html', {
        'labs': labs,
        'popular_tags': popular_tags
    })


@login_required
def labs(request):
    all_labs = Lab.get_published()
    return _labs(request, all_labs)


@login_required
def labsByUser(request):
    all_labs = Lab.objects.filter(mgr_id=request.user,
                                    status=Lab.PUBLISHED)
    return _labs(request, all_labs)



@login_required
def lab(request, slug):
    lab = get_object_or_404(Lab, slug=slug, status=Lab.PUBLISHED)
    return render(request, 'labs/lab.html', {'lab': lab})


@login_required
def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    labs = []
    for tag in tags:
        if tag.lab.status == Lab.PUBLISHED:
            labs.append(tag.lab)
    return _labs(request, labs)


# def persist_collaborators(collaborators, proj):
#     #collaborators is a list, for each request we need to persist them
#     userMap = all_users.getUserDictionary()
#     for each in collaborators:
#         t, created = Collaborator.objects.get_or_create(project = proj,
#                                                         user = userMap[each])
        
@login_required
def write(request):
    if request.method == 'POST':
        form = LabForm(request.POST)
        if form.is_valid():
            lab = Lab()
            lab.create_user = request.user
            lab.title = form.cleaned_data.get('title')
            lab.description = form.cleaned_data.get('description')
#             collaborators = form.cleaned_data.get('collaborators')
#             collaborators.append(request.user.username)
#             collaborators = set(collaborators)
#             
#             print "The collaborators are: "            
#             print collaborators
#             
            status = form.cleaned_data.get('status')
            if status in [Lab.PUBLISHED, Lab.DRAFT]:
                lab.status = form.cleaned_data.get('status')
            lab.save()
#             persist_collaborators(collaborators, project)
            tags = form.cleaned_data.get('tags')
            lab.create_tags(tags)
            
            #get devices
#             material =  request.POST.getlist('material[]')
#             category = request.POST.getlist('category[]')
#             for i in range(len(material)):
#                 toInsert = Material()
#                 toInsert.name = material[i]
#                 toInsert.category = category[i]
#                 toInsert.project = project
#                 toInsert.save()
            
            return redirect('/labs/')
    else:
        print "rendering init form"
        form = LabForm()
    return render(request, 'labs/write.html', {'form': form})


@login_required
def drafts(request):
    drafts = Lab.objects.filter(create_user=request.user,
                                    status=Lab.DRAFT)
    return render(request, 'labs/drafts.html', {'drafts': drafts})


@login_required
def edit(request, id):
    tags = ''
    if id:
        lab = get_object_or_404(Lab, pk=id)
        for tag in lab.get_tags():
            tags = '{0} {1}'.format(tags, tag.tag)
        tags = tags.strip()
    else:
        lab = Lab(create_user=request.user)

    if request.user.username!= lab.mgr_id:
        messages.add_message(request, messages.ERROR,
                                 'You are not authorized to edit this lab page- ' + lab.name + '. Only Lab Manager is authorized to edit this page')
        return redirect('/labs/')

    if request.POST:
        form = LabForm(request.POST, instance=lab)
        if form.is_valid():
            form.save()
            lab.delete_tags()
#             project.delete_collaborators()
#             collaborators = form.cleaned_data.get('collaborators')
            tags = form.cleaned_data.get('tags')
#             persist_collaborators(collaborators, project)
            lab.create_tags(tags)
            return redirect('/labs/')
    else:
        form = LabForm(instance=lab)
        form.fields['tags'].initial = tags
#         form.fields['collaborators'].initial = collaborators
        
    return render(request, 'labs/edit.html', {'form': form})


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
