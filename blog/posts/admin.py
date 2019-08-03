from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Comment, Post, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ('name',)


def make_published(modeladmin, request, queryset):
    queryset.filter(status=Post.DRAFT).update(status=Post.PUBLISHED)


make_published.short_description = _('Mark selected as published')


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status', 'publish', 'created']
    actions = [make_published]
    search_fields = ('title', 'slug', 'body')
    list_filter = ['status', 'publish']
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'post', 'status', 'author', 'created']
    list_filter = ['post__title', 'created', 'status']
    search_fields = ('post__title', 'message')


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
