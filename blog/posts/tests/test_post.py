from datetime import timedelta

from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

from posts.models import Post


class PostBaseTestCase(TestCase):

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
        self.user = User.objects.create_user(
            username='test',
            password='password',
            is_staff=True,
        )


class PostModelTestCase(PostBaseTestCase):

    def test_manager(self):
        active = set(Post.active.values_list('title', flat=True))
        self.assertEqual(active, {'test1', 'test3'})

        published = set(Post.published.values_list('title', flat=True))
        self.assertEqual(published, {'test1'})

        all_items = set(Post.objects.values_list('title', flat=True))
        self.assertEqual(all_items, {'test1', 'test2', 'test3', 'test4'})


class PostViewTestCase(PostBaseTestCase):

    def _test_list(self, included, excluded):
        tpl = '<a href="{}">{}</a>'
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

        posts = Post.objects.filter(slug__in=included)
        for post in posts:
            self.assertContains(resp, tpl.format(post.url, post.title), html=True)

        posts = Post.objects.filter(slug__in=excluded)
        for post in posts:
            self.assertNotContains(resp, tpl.format(post.url, post.title), html=True)

    def _test_detail(self, included, excluded):
        tpl = '<title>{}</title>'
        posts = Post.objects.filter(slug__in=included)
        for post in posts:
            resp = self.client.get(post.url)
            self.assertEqual(resp.status_code, 200, post.title)
            self.assertContains(resp, tpl.format(post.title), html=True)

        posts = Post.objects.filter(slug__in=excluded)
        for post in posts:
            resp = self.client.get(post.url)
            self.assertEqual(resp.status_code, 404, post.title)

    def test_list(self):
        included = ['test1']
        excluded = ['test2', 'test3', 'test4']
        self._test_list(included, excluded)

    def test_list_staff(self):
        included = ['test1', 'test2', 'test3', 'test4']
        excluded = []
        self.assertTrue(self.client.login(username=self.user.username, password='password'))
        self._test_list(included, excluded)

    def test_detail(self):
        included = ['test1']
        excluded = ['test2', 'test3', 'test4']
        self._test_detail(included, excluded)

    def test_detail_staff(self):
        included = ['test1', 'test2', 'test3', 'test4']
        excluded = []
        self.assertTrue(self.client.login(username=self.user.username, password='password'))
        self._test_detail(included, excluded)


class AdditionalPagesTestCase(PostBaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        site = Site.objects.get(pk=settings.SITE_ID)
        self.flat_page = FlatPage.objects.create(
            url='/about/',
            title='About',
            content='about',
        )
        self.flat_page.sites.add(site)

    def test_about(self):
        url = reverse('about')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        tpl = '<title>{} - {}</title>'
        self.assertContains(resp, tpl.format(settings.BLOG_TITLE, self.flat_page.title), html=True)

    def test_feed(self):
        url = reverse('feed')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'test1')

    def test_sitemap(self):
        url = reverse('sitemap')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'test1')
