from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.translation import gettext as _

from posts.models import Post


class LatestPostsFeed(Feed):
    """RSS feed, based on https://docs.djangoproject.com/en/2.2/ref/contrib/syndication/"""
    title = settings.BLOG_TITLE
    link = '/'
    description = _('New posts')

    def items(self):
        return Post.published.all()[:settings.POSTS_PER_RSS]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body
