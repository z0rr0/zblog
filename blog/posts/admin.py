from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Post, Tag, Comment


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']


def make_published(modeladmin, request, queryset):
    queryset.filter(status=Post.DRAFT).update(status=Post.PUBLISHED)


make_published.short_description = _('Mark selected as published')


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status', 'published', 'created']
    actions = [make_published]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'post', 'author', 'like', 'dislike', 'created']


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
