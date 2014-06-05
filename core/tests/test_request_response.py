"""
Functional tests that go through the full request response cycle.
They test HTML templates, middlewares and views.
"""
from ndbtestcase import AppEngineTestCase
from django.core.urlresolvers import reverse

from core.models import Blog, Article


class TestIndexPage(AppEngineTestCase):
    url = reverse('index')

    def setUp(self):
        Blog(title="my_blog_title").put()

    def test_correct_template_loaded(self):
        resp = self.client.get(self.url)
        self.assertTemplateUsed(
            template_name="index.html",
            response=resp
        )

    def test_200_and_name_in_page(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, "my_blog_title")

    def test_no_articles(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, "This blog looks empty!")

    def test_with_articles(self):
        Article(title="title_article_one").put()
        Article(title="title_article_two").put()
        resp = self.client.get(self.url)
        self.assertContains(resp, "title_article_one")
        self.assertContains(resp, "title_article_two")


class TestManageArticlesPage(AppEngineTestCase):
    url = reverse('article_admin_list')

    def setUp(self):
        Blog(title="my_blog_title").put()

    def test_user_not_admin(self):
        self.users_login('user@localhost', is_admin=False)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_user_not_authenticated(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_correct_template_loaded(self):
        self.users_login('admin@localhost', is_admin=True)
        resp = self.client.get(self.url)
        self.assertTemplateUsed(
            template_name="article_admin_list.html",
            response=resp
        )

    def test_no_articles(self):
        self.users_login('admin@localhost', is_admin=True)
        resp = self.client.get(self.url)
        self.assertContains(resp, "This blog looks empty!")

    def test_with_articles(self):
        self.users_login('admin@localhost', is_admin=True)
        Article(title="title_article_one").put()
        Article(title="title_article_two").put()

        resp = self.client.get(self.url)

        self.assertContains(resp, "title_article_one")
        self.assertContains(resp, "title_article_two")


class TestArticleCreatePage(AppEngineTestCase):
    url = reverse('article_admin_create')

    def setUp(self):
        Blog(title="my_blog_title").put()

    def test_user_not_admin(self):
        self.users_login('user@localhost', is_admin=False)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_user_not_authenticated(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_correct_template_loaded(self):
        self.users_login('admin@localhost', is_admin=True)
        resp = self.client.get(self.url)
        self.assertTemplateUsed(
            template_name="article_admin_create.html",
            response=resp
        )

    def test_200_and_name_in_page(self):
        self.users_login('admin@localhost', is_admin=True)
        resp = self.client.get(self.url)
        self.assertContains(resp, "my_blog_title")

    def test_post_valid(self):
        self.users_login('admin@localhost', is_admin=True)
        data = {
            'title': 'article_title',
            'body': 'article_body'
        }

        resp = self.client.post(self.url, data)

        self.assertRedirects(resp, reverse('index'))
        self.assertEqual(Article.all().count(), 1)

    def test_post_invalid_missing_body(self):
        self.users_login('admin@localhost', is_admin=True)
        data = {'title': 'article_title'}

        resp = self.client.post(self.url, data)

        self.assertContains(resp, 'This field is required')
        self.assertEqual(Article.all().count(), 0)

    def test_post_invalid_missing_title(self):
        self.users_login('admin@localhost', is_admin=True)
        data = {'body': 'article_body'}

        resp = self.client.post(self.url, data)

        self.assertContains(resp, 'This field is required')
        self.assertEqual(Article.all().count(), 0)
