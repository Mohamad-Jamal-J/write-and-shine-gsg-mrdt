from django.contrib import admin

from posts.models import Post, Tag
from interactions.models import Comment, Like


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Like)