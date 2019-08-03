from django.urls import path
from django.views.decorators.vary import vary_on_cookie

from posts.views import PostDetailView, PostListView

urlpatterns = [
    path('', vary_on_cookie(PostListView.as_view()), name='index'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', vary_on_cookie(PostDetailView.as_view()), name='read'),
    path('tag/<slug:tag>', vary_on_cookie(PostListView.as_view()), name='tag_filter'),
]
