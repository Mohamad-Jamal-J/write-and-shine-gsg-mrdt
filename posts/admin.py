from django.contrib import admin

from posts.models import Comment, Like, Post, Post_tag, Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Post_tag)
admin.site.register(Comment)
admin.site.register(Like)