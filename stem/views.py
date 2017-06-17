import os
from django.contrib.auth.decorators import permission_required
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.static import serve

from easygoing import settings
from stem.forms import CommentForm, UserCommentForm, WebsiteForm, EditPostForm, UploadFileForm
from stem.models import Website
from stem.services import get_main_context, get_blog_posts, get_post, submit_comment, close_comments, \
    takedown_comment, get_file, file_hide, post_hide


def index(request):
    context = get_main_context()
    posts = get_blog_posts(True if request.user.has_perm('stem.change_post') else False)
    paginator = Paginator(posts, context['website'].page_size)
    page = request.GET.get('page')
    try:
        context['posts'] = paginator.page(page)
    except PageNotAnInteger:
        context['posts'] = paginator.page(1)
    except EmptyPage:
        context['posts'] = paginator.page(paginator.num_pages)
    return render(request, 'stem/index.html', context)


@permission_required('stem.change_website')
def edit_home(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST, request.FILES, instance=Website.get_solo())
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = WebsiteForm(instance=Website.get_solo())
    context = get_main_context()
    context['form'] = form
    return render(request, 'stem/edit_home.html', context)


@permission_required('stem.add_post')
def new_post(request):
    if request.method == 'POST':
        form = EditPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            id = post.pk
            return redirect(reverse('post', args=[id]))
    else:
        form = EditPostForm()
    context = get_main_context()
    context['form'] = form
    return render(request, 'stem/edit_post.html', context)


@permission_required('stem.add_post')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.save()
            return redirect(reverse('present_file', args=[file.uuid]))
        else:
            print(form)
            print(request.POST)
            print(request.FILES)
    else:
        form = UploadFileForm()
    context = get_main_context()
    context['form'] = form
    return render(request, 'stem/upload_file.html', context)


def present_file(request, uuid):
    file = get_file(uuid)
    if not request.user.is_authenticated and file.hidden:
        return redirect('login')
    context = get_main_context()
    context['file'] = file
    return render(request, 'stem/present_file.html', context)


def serve_file(request, uuid):
    file = get_file(uuid)
    if not request.user.is_authenticated and file.hidden:
        return redirect('login')

    if not settings.DEBUG:
        response = HttpResponse()
        response["Content-Disposition"] = "attachment; filename={0}".format(file.filename)
        response['X-Accel-Redirect'] = f"{settings.MEDIA_URL}/{uuid}"
        return response
    else:
        filepath = os.path.join(settings.MEDIA_ROOT, uuid)
        response = serve(request, os.path.basename(filepath), os.path.dirname(filepath))
        response["Content-Disposition"] = "attachment; filename={0}".format(file.filename)
        return response


def post(request, id):
    post = get_post(id)
    if not request.user.is_authenticated and post.hidden:
        return redirect('login')
    if request.method == 'POST':
        form = UserCommentForm(request.POST) if request.user.is_authenticated else CommentForm(request.POST)
        if form.is_valid():
            submit_comment(id,
                           request.user if request.user.is_authenticated else None,
                           form.cleaned_data)
            return redirect('post', id)
    else:
        form = UserCommentForm() if request.user.is_authenticated else CommentForm()
    context = get_main_context()
    context['post'] = post
    context['form'] = form
    return render(request, 'stem/post.html', context)


@permission_required('stem.change_post')
def edit(request, id):
    post = get_post(id)
    if request.method == 'POST':
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(edit=True)
            return redirect(reverse('post', args=[id]))
    else:
        form = EditPostForm(instance=post)
    context = get_main_context()
    context['form'] = form
    return render(request, 'stem/edit_post.html', context)


@permission_required('stem.change_post')
def hide_post(request, id):
    if request.method == 'POST':
        post_hide(id)
    return redirect('post', id)


@permission_required('stem.change_post')
def hide_file(request, uuid):
    if request.method == 'POST':
        file_hide(uuid)
    return redirect('present_file', uuid)


@permission_required('stem.change_post')
def close(request, id):
    if request.method == 'POST':
        close_comments(id)
    return redirect('post', id)


@permission_required('stem.change_comment')
def takedown(request, id):
    if request.method == 'POST':
        post_id = takedown_comment(id)
    return redirect(reverse('post', args=[post_id]) + f'#comment-{id}')
