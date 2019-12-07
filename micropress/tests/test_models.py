from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Press, Section, Article

from sample_project.app_one.models import OneGame
from sample_project.app_two.models import TwoGame


class PressTestCase(TestCase):
    def test_association(self):
        realm = OneGame.objects.create(slug='test')

        press = Press.objects.create(
            name="The Ulfland Gazette",
            realm=realm,
        )

        self.assertEqual(Press.objects.count(), 1)
        self.assertEqual(press.realm, realm)

    def test_multiple_apps(self):
        realm1 = OneGame.objects.create(slug='one')
        press1 = Press.objects.create(
            name="The Ulfland Gazette",
            realm=realm1
        )
        realm2 = TwoGame.objects.create(slug='two')
        press2 = Press.objects.create(
            name="The Times New Roman",
            realm=realm2
        )

        self.assertEqual(Press.objects.count(), 2)
        self.assertEqual(press1.realm, realm1)
        self.assertEqual(press2.realm, realm2)


class ArticleTestCase(TestCase):
    def test_can_have_article(self):
        realm = OneGame.objects.create(slug='test')
        user = User.objects.create_user('bob', 'bob@example.com', 'password')

        press = Press.objects.create(
            name="The Ulfland Gazette",
            realm=realm,
        )
        section = Section.objects.create(name='Hometown')
        article = Article.objects.create(
            press=press,
            author=user,
            section=section,
            title="Hello World!",
            byline="Anonymous",
            body="Hello.",
        )
        press = Press.objects.get()

        self.assertEqual(press.article_set.count(), 1)
        article = press.article_set.get()
        self.assertEqual(article.slug, 'hello-world')
        self.assertEqual(article.body_html, '<p>Hello.</p>\n')
