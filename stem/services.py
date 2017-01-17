from stem.models import Website, Post

DEFAULT_PAGE_SIZE = 15
DEFAULT_TRUNCATE_LIMIT = 200


def get_main_context():
    website = Website.get_solo()
    context = {'title': website.title, 'sidebar': website.sidebar, 'header': website.header,
               'truncate_word_limit': website.truncate_word_limit or DEFAULT_TRUNCATE_LIMIT,
               'page_size': website.page_size or DEFAULT_PAGE_SIZE}
    return context


def get_blog_posts(show_all=False):
    posts = Post.objects.filter(blog_post=True).order_by('-created')
    # if not show_all:
    #     posts = posts.filter(hidden=False)
    return posts


def get_post(id):
    post = Post.objects.filter(pk=id).prefetch_related('comment_set')[0]
    return post
