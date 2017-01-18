from django.contrib.auth.decorators import permission_required
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from stem.forms import CommentForm
from stem.services import get_main_context, get_blog_posts, get_post, submit_comment, hide_post, close_comments, \
    takedown_comment, edit_post, create_post


def index(request):
    context = get_main_context()
    posts = get_blog_posts(True if request.user.has_perm('stem.change_post') else False)
    paginator = Paginator(posts, context['page_size'])
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
        edit_post(id, 'dummy', 'dummycontent')
        return redirect('post', id)
    else:
        # TODO edit post iterface
        pass


@permission_required('stem.add_post')
def new_post(request):
    if request.method == 'POST':
        id = create_post(request.user)
        return redirect('edit_post', id)
    else:
        return redirect('index')


def post(request, id):
    post = get_post(id)
    if not request.user.is_authenticated and post.hidden:
        return redirect('login')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            submit_comment(id,
                           request.user if request.user.is_authenticated else None,
                           form.cleaned_data)
            return redirect('post', id)
    else:
        form = CommentForm()
    context = get_main_context()
    context['post'] = post
    context['form'] = form
    return render(request, 'stem/post.html', context)


@permission_required('stem.change_post')
def edit(request, id):
    if request.method == 'POST':
        edit_post(id, 'dummy', 'dummycontent')
        return redirect('post', id)
    else:
        # TODO edit post iterface
        pass


@permission_required('stem.change_post')
def hide(request, id):
    if request.method == 'POST':
        hide_post(id)
    return redirect('post', id)


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
