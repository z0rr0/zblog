from django.contrib.syndication.views import Feed

from posts.models import Post


class LatestPostsFeed(Feed):
    """RSS feed, based on https://docs.djangoproject.com/en/2.2/ref/contrib/syndication/"""
    title = 'Zblog posts'
    link = '/'
    description = 'New posts.'
    limit = 10

    def items(self):
        return Post.published.all()[:self.limit]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body
