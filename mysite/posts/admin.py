from django.contrib import admin
from .models import Video, Post, MoreVideoPost, Comment

admin.site.register(Video)
admin.site.register(Post)
admin.site.register(MoreVideoPost)
admin.site.register(Comment)