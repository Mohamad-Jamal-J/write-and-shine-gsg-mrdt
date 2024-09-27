from django.contrib import admin

from posts.models import Comment, Like, Post, Post_Tag, Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Post_Tag)
admin.site.register(Comment)
admin.site.register(Like)