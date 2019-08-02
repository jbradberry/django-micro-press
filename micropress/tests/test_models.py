from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Press, Section, Article

from sample_project.sample_app.models import TestRealm


class PressTestCase(TestCase):
    def test_association(self):
        realm = TestRealm.objects.create(slug='test')

        press = Press.objects.create(
            name="The Ulfland Gazette",
            realm=realm,
        )

        self.assertEqual(Press.objects.count(), 1)
        self.assertEqual(press.realm, realm)


class ArticleTestCase(TestCase):
    def test_can_have_article(self):
        realm = TestRealm.objects.create(slug='test')
        author = User.objects.create(username='bob')

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
        press = Press.objects.get()

        self.assertEqual(press.article_set.count(), 1)
        article = press.article_set.get()
        self.assertEqual(article.slug, 'hello-world')
        self.assertEqual(article.body_html, '<p>Hello.</p>\n')
