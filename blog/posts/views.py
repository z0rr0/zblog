from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView

from posts.models import Post, Tag


class StaffViewMixin:

    @property
    def is_authenticated_staff(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.is_authenticated_staff:
            queryset = Post.published.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_staff'] = self.is_authenticated_staff
        return context


class PostListView(StaffViewMixin, ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = settings.POSTS_PER_PAGE
    template_name = 'blog/post/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # add tags and user
        context['tags'] = Tag.objects.all()
        return context


class PostDetailView(StaffViewMixin, DetailView):
    queryset = Post.objects.all()
    context_object_name = 'post'
    template_name = 'blog/post/detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            publish__year=self.kwargs['year'],
            publish__month=self.kwargs['month'],
            publish__day=self.kwargs['day'],
        )
        return queryset


def about(request: HttpRequest):
    """Returns author about page"""
    return HttpResponse('about')


def comment_add(request: HttpRequest, post_id: int):
    """Adds new comment for a post"""
    return HttpResponse('comment_add')
