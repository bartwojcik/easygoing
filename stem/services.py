from datetime import datetime

from django.core.exceptions import PermissionDenied

from stem.models import Website, Post, Comment

DEFAULT_PAGE_SIZE = 15
DEFAULT_TRUNCATE_LIMIT = 200


def get_main_context():
    website = Website.get_solo()
    context = {'title': website.title,
               'header': website.header,
               'sidebar': website.sidebar,
               'footer': website.footer,
               'truncate_word_limit': website.truncate_word_limit or DEFAULT_TRUNCATE_LIMIT,
               'page_size': website.page_size or DEFAULT_PAGE_SIZE}
    return context


def get_blog_posts(show_all=False):
    posts = Post.objects.filter(blog_post=True).order_by('-created')
    if not show_all:
        posts = posts.filter(hidden=False)
    return posts


def get_post(id):
    post = Post.objects.filter(pk=id).prefetch_related('comment_set')[0]
    return post


def submit_comment(post_id, user, form_data):
    post = Post.objects.get(pk=post_id)
    if post.hidden and (user is None or not user.has_perm('stem.change_post')) or post.comments_closed:
        raise PermissionDenied('Post is hidden or comments are closed')
    comment = Comment()
    comment.content = form_data['content']
    comment.post = post
    if user is not None:
        comment.author = user
    else:
        if not form_data['author_name']:
            raise TypeError('Author name form data element or user argument must be provided')
        else:
            comment.author_name = form_data['author_name']
            comment.author_email = form_data['author_email']
    comment.date = datetime.now()
    comment.taken_down = False
    comment.post.number_of_comments += 1
    comment.post.save()
    comment.save()


def create_post(user):
    post = Post()
    post.author = user
    post.created = datetime.now()
    post.language = 'en'
    post.title = 'Enter post title here'
    post.content = 'Enter post content here'
    post.blog_post = False
    post.hidden = True
    post.comments_closed = False
    post.number_of_comments = 0
    post.save()
    return post.pk


def edit_post(post_id, post_title, post_content):
    post = Post.objects.get(pk=post_id)
    post.edited = datetime.now()
    post.title = post_title
    post.content = post_content
    post.save()


def hide_post(post_id):
    post = Post.objects.get(pk=post_id)
    post.hidden = not post.hidden
    post.save()


def close_comments(post_id):
    post = Post.objects.get(pk=post_id)
    post.comments_closed = not post.comments_closed
    post.save()


def takedown_comment(comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if comment.taken_down:
        comment.post.number_of_comments += 1
        comment.taken_down = False
    else:
        comment.post.number_of_comments -= 1
        comment.taken_down = True
    comment.post.save()
    comment.save()
    return comment.post.pk


def edit_website():
    pass
