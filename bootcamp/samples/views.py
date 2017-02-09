from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.contrib import messages

import bootcamp.core.all_users as all_users
import markdown
from bootcamp.samples.forms import SampleForm
from bootcamp.samples.models import Sample, SampleComment, Tag
from bootcamp.decorators import ajax_required

PROJECTS_NUM_PAGES = 100


def _samples(request, samples):
    paginator = Paginator(samples, 100)
    page = request.GET.get('page')
    try:
        samples = paginator.page(page)
    except PageNotAnInteger:
        samples = paginator.page(1)
    except EmptyPage:
        samples = paginator.page(paginator.num_pages)
    popular_tags = Tag.get_popular_tags()
    print samples
    return render(request, 'samples/samples.html', {
        'samples': samples,
        'popular_tags': popular_tags
    })


@login_required
def samples(request):
    all_samples = Sample.get_published()
    return _samples(request, all_samples)


@login_required
def samplesByUser(request):
    all_samples = Sample.objects.filter(create_user=request.user,
                                        status=Sample.PUBLISHED)
    return _samples(request, all_samples)


@login_required
def sample(request, slug):
    print "reached here"
    sample = get_object_or_404(Sample, slug=slug, status=Sample.PUBLISHED)
    print "This is the sample", sample
    return render(request, 'samples/sample.html', {'sample': sample})


@login_required
def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    samples = []
    for tag in tags:
        if tag.sample.status == Sample.PUBLISHED:
            samples.append(tag.sample)
    return _samples(request, samples)


@login_required
def add(request):
    if request.method == 'POST':
        form = SampleForm(request.POST)
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
        print "rendering init form"
        form = SampleForm()
    return render(request, 'samples/add.html', {'form': form})


@login_required
def drafts(request):
    drafts = Sample.objects.filter(create_user=request.user,
                                   status=Sample.DRAFT)
    return render(request, 'samples/drafts.html', {'drafts': drafts})


@login_required
def edit(request, id):
    print "Ok reached here"
    tags = ''
    if id:
        sample = get_object_or_404(Sample, pk=id)
        for tag in sample.get_tags():
            tags = '{0} {1}'.format(tags, tag.tag)
        tags = tags.strip()
    else:
        sample = Sample(create_user=request.user)

    # if request.user.username not in collaborators:
    #     messages.add_message(request, messages.ERROR,
    #                          'You are not authorized to edit this Sample- ' + sample.title + '. Only collaborators can edit their Sample')
    #     return redirect('/samples/')

    if request.POST:
        form = SampleForm(request.POST, instance=sample)
        if form.is_valid():
            form.save()
            sample.delete_tags()
            sample.delete_collaborators()
            tags = form.cleaned_data.get('tags')
            sample.create_tags(tags)
            return redirect('/samples/')
    else:
        form = SampleForm(instance=sample)
        form.fields['tags'].initial = tags
        print form
    return render(request, 'samples/edit.html', {'form': form})


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
            sample_id = request.POST.get('sample')
            sample = Sample.objects.get(pk=sample_id)
            comment = request.POST.get('comment')
            comment = comment.strip()
            if len(comment) > 0:
                sample_comment = SampleComment(user=request.user,
                                               sample=sample,
                                               comment=comment)
                sample_comment.save()
            html = ''
            for comment in sample.get_comments():
                html = '{0}{1}'.format(html, render_to_string(
                    'samples/partial_sample_comment.html',
                    {'comment': comment}))

            return HttpResponse(html)

        else:
            return HttpResponseBadRequest()

    except Exception:
        return HttpResponseBadRequest()
