from django.conf import settings
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView

from posts.models import Post


class StaffViewMixin:

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.is_staff_user:
            queryset = Post.published.all()
        return queryset


class PostListView(StaffViewMixin, ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = settings.POSTS_PER_PAGE
    template_name = 'blog/post/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        search = self.request.GET.get('search')
        tag = self.kwargs.get('tag')
        if search:
            info = _('Search result for keyword')
            context['info'] = f'{info} "{search}"'
        elif tag:
            info = _('Search by tag')
            context['info'] = f'{info} "{tag}"'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search is not None:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search) |
                Q(tags__name__iexact=search)
            )
        tag = self.kwargs.get('tag')
        if tag is not None:
            queryset = queryset.filter(tags__name__iexact=tag)
        return queryset


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
