from django.conf import settings
from django.db.models import Count

from posts.models import Tag


class BlogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # tags cloud
        request.tags = Tag.published.values('name').annotate(count=Count('posts__pk')).order_by('-count')
        # user staff flag
        request.is_staff_user = request.user.is_authenticated and request.user.is_staff
        # footer links
        request.settings_params = {
            'github': settings.GITHUB_LINK,
            'title': settings.BLOG_TITLE,
        }

        response = self.get_response(request)
        return response
