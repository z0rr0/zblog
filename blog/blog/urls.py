"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.contrib.flatpages import views
from django.contrib.sitemaps.views import sitemap
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps import GenericSitemap
from posts.models import Post
from posts.feed import LatestPostsFeed


posts_sitemap_info = {
    'queryset': Post.published.all(),
    'date_field': 'publish',
}

urlpatterns = [
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('admin/', admin.site.urls),
    path('feed/', LatestPostsFeed(), name='feed'),
    path('', include('posts.urls')),
    # the sitemap
    path(
        'sitemap.xml', sitemap,
        {
            'sitemaps': {
                'flatpages': FlatPageSitemap,
                'posts': GenericSitemap(posts_sitemap_info, priority=0.6),
            },
        },
        name='sitemap',
    ),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
