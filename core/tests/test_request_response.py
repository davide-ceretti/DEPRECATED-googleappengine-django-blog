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
        Article(title="title_article_one", body="body_one").put()
        Article(title="title_article_two",  body="body_two").put()
        resp = self.client.get(self.url)
        self.assertContains(resp, "title_article_one")
        self.assertContains(resp, "title_article_two")

    def test_visible_menu_when_admin(self):
        self.users_login('admin@localhost', is_admin=True)
        resp = self.client.get(self.url)
        self.assertContains(resp, "Index")
        self.assertContains(resp, "Manage articles")
        self.assertContains(resp, "Manage blog")
        self.assertContains(resp, "Add article")
        self.assertContains(resp, "Logout")
        self.assertNotContains(resp, "Login")

    def test_visible_menu_when_not_admin(self):
        self.users_login('user@localhost', is_admin=False)
        resp = self.client.get(self.url)
        self.assertContains(resp, "Index")
        self.assertContains(resp, "Logout")
        self.assertNotContains(resp, "Login")
        self.assertNotContains(resp, "Manage articles")
        self.assertNotContains(resp, "Manage blog")
        self.assertNotContains(resp, "Add article")

    def test_visible_menu_when_not_authenticated(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, "Index")
        self.assertContains(resp, "Login")
        self.assertNotContains(resp, "Manage articles")
        self.assertNotContains(resp, "Manage blog")
        self.assertNotContains(resp, "Add article")
        self.assertNotContains(resp, "Logout")


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
        Article(title="title_article_one", body="body_one").put()
        Article(title="title_article_two",  body="body_two").put()

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


class TestUpdateBlog(AppEngineTestCase):
    url = reverse('blog_admin_update')

    def setUp(self):
        Blog(title="my_blog_title").put()

    def test_user_not_admin(self):
        self.users_login('user@localhost', is_admin=False)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_user_not_authenticated(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_200_and_form_in_page(self):
        self.users_login('admin@localhost', is_admin=True)
        resp = self.client.get(self.url)
        self.assertContains(resp, "Title")

    def test_post_no_title(self):
        self.users_login('admin@localhost', is_admin=True)
        data = {'title': ''}

        resp = self.client.post(self.url, data)

        self.assertContains(resp, 'This field is required')
        self.assertEqual(Blog.get_unique().title, 'my_blog_title')

    def test_post_valid(self):
        self.users_login('admin@localhost', is_admin=True)
        data = {'title': 'new_blog_title'}

        resp = self.client.post(self.url, data)

        self.assertRedirects(resp, reverse('index'))
        self.assertEqual(Blog.get_unique().title, 'new_blog_title')


class TestDeleteArticle(AppEngineTestCase):
    def setUp(self):
        Blog(title="my_blog_title").put()

    def test_user_not_admin(self):
        Article(title='title', body='body').put()
        self.users_login('user@localhost', is_admin=False)
        url = reverse('article_admin_delete', kwargs={'id': 1})

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Article.all().count(), 1)

    def test_user_not_authenticated(self):
        Article(title='title', body='body').put()
        url = reverse('article_admin_delete', kwargs={'id': 1})

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Article.all().count(), 1)

    def test_article_does_not_exist(self):
        Article(key_name='randomkey', title='title', body='body').put()
        self.users_login('admin@localhost', is_admin=True)
        url = reverse('article_admin_delete', kwargs={'id': 1})

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(Article.all().count(), 1)

    def test_article_exist(self):
        key = Article(title='title', body='body').put()
        self.users_login('admin@localhost', is_admin=True)
        url = reverse('article_admin_delete', kwargs={'id': key.id()})

        resp = self.client.get(url)

        self.assertRedirects(resp, reverse('article_admin_list'))
        self.assertEqual(Article.all().count(), 0)
