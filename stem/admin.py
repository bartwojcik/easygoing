from django.contrib import admin

from stem.models import Website, Post, Comment, UploadedFile

admin.site.register(Website)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UploadedFile)
