from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render

from stem.services import get_main_context, get_blog_posts, get_post


def index(request):
    context = get_main_context()
    # TODO check if admin and add hidden posts
    posts = get_blog_posts()
    paginator = Paginator(posts, context['page_size'])
    page = request.GET.get('page')
    try:
        context['posts'] = paginator.page(page)
    except PageNotAnInteger:
        context['posts'] = paginator.page(1)
    except EmptyPage:
        context['posts'] = paginator.page(paginator.num_pages)
    return render(request, 'stem/index.html', context)


def post(request, id):
    context = get_main_context()
    context['post'] = get_post(id)
    return render(request, 'stem/post.html', context)
