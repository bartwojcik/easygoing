from django.contrib import admin

from stem.models import Website, Article, Comment

admin.site.register(Website)
admin.site.register(Article)
admin.site.register(Comment)
