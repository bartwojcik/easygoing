from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<id>[0-9]*)/$', views.post, name='post'),
]
