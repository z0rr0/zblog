from django.urls import path

from posts.views import PostDetailView, PostListView


urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='read'),
    path('tag/<slug:tag>', PostListView.as_view(), name='tag_filter'),
]
