from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit_home/$', views.edit_home, name='edit_home'),
    url(r'^new_post/$', views.new_post, name='new_post'),
    url(r'^post/(?P<id>[0-9]*)/$', views.post, name='post'),
    url(r'^edit_post/(?P<id>[0-9]*)/$', views.edit, name='edit_post'),
    url(r'^hide_post/(?P<id>[0-9]*)/$', views.hide, name='hide_post'),
    url(r'^close_post/(?P<id>[0-9]*)/$', views.close, name='close_post'),
    url(r'^takedown_comment/(?P<id>[0-9]*)/$', views.takedown, name='takedown_comment'),
]
