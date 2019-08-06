from django.conf import settings
from django.db.models import Count

from posts.models import Tag


class BlogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # user staff flag
        request.is_staff_user = request.user.is_authenticated and request.user.is_staff

        # tags cloud
        tags_qs = Tag.objects.all() if request.is_staff_user else Tag.published.all()
        request.tags = tags_qs.values('name').annotate(count=Count('posts__pk')).order_by('-count')

        # settings configuration params
        request.settings_params = {
            'github': settings.GITHUB_LINK,
            'title': settings.BLOG_TITLE,
            'meta_description': settings.META_DESCRIPTION,
            'meta_author': settings.META_AUTHOR,
            'lang': settings.LANGUAGE_CODE.split('-', 1)[0],
        }

        response = self.get_response(request)
        return response
