from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from ..models import Press, Section, Article

from sample_project.sample_app.models import TestRealm


class ArticleListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_basic(self):
        realm = TestRealm.objects.create(slug='test')
        author = User.objects.create_user('bob', 'bob@example.com', 'password')

        press = Press.objects.create(
            name="The Ulfland Gazette",
            realm=realm,
        )
        section = Section.objects.create(name='Hometown')
        article = Article.objects.create(
            press=press,
            author=author,
            section=section,
            title="Hello World!",
            byline="Anonymous",
            body="Hello.",
        )

        try:
            url = reverse(
                'article_list',
                kwargs={'realm_content_type': 'sample_app.testrealm', 'realm_slug': 'test'}
            )
        except Exception as e:
            self.fail(e)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ArticleDetailViewTestCase(TestCase):
    def test_basic(self):
        realm = TestRealm.objects.create(slug='test')
        author = User.objects.create_user('bob', 'bob@example.com', 'password')

        press = Press.objects.create(
            name="The Ulfland Gazette",
            realm=realm,
        )
        section = Section.objects.create(name='Hometown')
        article = Article.objects.create(
            press=press,
            author=author,
            section=section,
            title="Hello World!",
            byline="Anonymous",
            body="Hello.",
        )

        try:
            url = reverse(
                'article_detail',
                kwargs={'realm_content_type': 'sample_app.testrealm', 'realm_slug': 'test', 'slug': 'hello-world'}
            )
        except Exception as e:
            self.fail(e)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ArticleCreateViewTestCase(TestCase):
    def test_basic(self):
        realm = TestRealm.objects.create(slug='test')
        author = User.objects.create_user('bob', 'bob@example.com', 'password')

        press = Press.objects.create(
            name="The Ulfland Gazette",
            realm=realm,
        )
        section = Section.objects.create(name='Hometown')

        try:
            url = reverse(
                'article_create',
                kwargs={'realm_content_type': 'sample_app.testrealm', 'realm_slug': 'test'}
            )
        except Exception as e:
            self.fail(e)

        data = {}
        self.assertTrue(self.client.login(username=author.username, password='password'))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
