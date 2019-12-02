from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Press, Section, Article

from sample_project.app_one.models import OneGame


class ArticleListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_basic(self):
        realm = OneGame.objects.create(slug='test')
        author = User.objects.create_user('bob', 'bob@example.com', 'password')

        press = Press.objects.create(
            name="The Ulfland Gazette",
            realm=realm,
        )
        section = Section.objects.create(name='Hometown')
        Article.objects.create(
            press=press,
            author=author,
            section=section,
            title="Hello World!",
            byline="Anonymous",
            body="Hello.",
        )

        try:
            url = reverse(
                'app_one:article_list',
                kwargs={'realm_slug': 'test'}
            )
        except Exception as e:
            self.fail(e)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ArticleDetailViewTestCase(TestCase):
    def test_basic(self):
        realm = OneGame.objects.create(slug='test')
        author = User.objects.create_user('bob', 'bob@example.com', 'password')

        press = Press.objects.create(
            name="The Ulfland Gazette",
            realm=realm,
        )
        section = Section.objects.create(name='Hometown')
        Article.objects.create(
            press=press,
            author=author,
            section=section,
            title="Hello World!",
            byline="Anonymous",
            body="Hello.",
        )

        try:
            url = reverse(
                'app_one:article_detail',
                kwargs={'realm_slug': 'test', 'slug': 'hello-world'}
            )
        except Exception as e:
            self.fail(e)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ArticleCreateViewTestCase(TestCase):
    def test_basic(self):
        realm = OneGame.objects.create(slug='test')
        author = User.objects.create_user('bob', 'bob@example.com', 'password')

        Press.objects.create(
            name="The Ulfland Gazette",
            realm=realm,
        )
        Section.objects.create(name='Hometown')

        try:
            url = reverse(
                'app_one:article_create',
                kwargs={'realm_slug': 'test'}
            )
        except Exception as e:
            self.fail(e)

        data = {'foo': 'bar'}
        self.assertTrue(self.client.login(username=author.username, password='password'))
        # import pdb; pdb.set_trace()
        response = self.client.post(url, data=data)
        # self.fail(response)
        self.assertEqual(response.status_code, 200)
