from django.conf.urls import url
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap

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
    url(r'^post/(?P<id>[0-9]*)/$', views.post, name='post'),
    url(r'^edit_post/(?P<id>[0-9]*)/$', views.edit, name='edit_post'),
    url(r'^hide_post/(?P<id>[0-9]*)/$', views.hide, name='hide_post'),
    url(r'^close_post/(?P<id>[0-9]*)/$', views.close, name='close_post'),
    url(r'^takedown_comment/(?P<id>[0-9]*)/$', views.takedown, name='takedown_comment'),
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'posts': PostsSitemap}},
        name='django.contrib.sitemaps.views.sitemap'),
]
