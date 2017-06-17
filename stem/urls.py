from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap

from easygoing import settings
from stem.models import Post
from . import views


class PostsSitemap(Sitemap):
    changefreq = 'weekly'  # (possibly in a distant future) add a setting to Post model and change this to method
    priority = 1

    def items(self):
        return Post.objects.filter(hidden=False)

    def lastmod(self, obj):
        return obj.edited


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit_home/$', views.edit_home, name='edit_home'),
    url(r'^new_post/$', views.new_post, name='new_post'),
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^post/(?P<id>[0-9]*)/$', views.post, name='post'),
    url(r'^present_file/(?P<uuid>[0-9abcdef]{32})/$', views.present_file, name='present_file'),
    url(r'^file/(?P<uuid>[0-9abcdef]{32})/$', views.serve_file, name='serve_file'),
    url(r'^edit_post/(?P<id>[0-9]*)/$', views.edit, name='edit_post'),
    url(r'^hide_post/(?P<id>[0-9]*)/$', views.hide_post, name='hide_post'),
    url(r'^hide_file/(?P<uuid>[0-9abcdef]{32})/$', views.hide_file, name='hide_file'),
    url(r'^close_post/(?P<id>[0-9]*)/$', views.close, name='close_post'),
    url(r'^takedown_comment/(?P<id>[0-9]*)/$', views.takedown, name='takedown_comment'),
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'posts': PostsSitemap}},
        name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
