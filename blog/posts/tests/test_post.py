from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from posts.models import Post


class PostModelTestCase(TestCase):

    def setUp(self) -> None:
        now = timezone.now()
        Post.objects.bulk_create([
            Post(
                title='test1',
                slug='test1',
                body='body',
                publish=now - timedelta(days=1),
                status=Post.PUBLISHED,
            ),
            Post(
                title='test2',
                slug='test2',
                body='body',
                publish=now - timedelta(days=1),
                status=Post.DRAFT,
            ),
            Post(
                title='test3',
                slug='test3',
                body='body',
                publish=now + timedelta(days=1),
                status=Post.PUBLISHED,
            ),
            Post(
                title='test4',
                slug='test4',
                body='body',
                publish=now - timedelta(days=1),
                status=Post.DELETED,
            ),
        ])

    def test_manager(self):
        active = set(Post.active.values_list('title', flat=True))
        self.assertEqual(active, {'test1', 'test3'})

        published = set(Post.published.values_list('title', flat=True))
        self.assertEqual(published, {'test1'})

        all_items = set(Post.objects.values_list('title', flat=True))
        self.assertEqual(all_items, {'test1', 'test2', 'test3', 'test4'})
