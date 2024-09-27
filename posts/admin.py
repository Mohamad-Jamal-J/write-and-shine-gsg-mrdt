from django.contrib import admin

from posts.models import Comment, Like, Post, Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Like)