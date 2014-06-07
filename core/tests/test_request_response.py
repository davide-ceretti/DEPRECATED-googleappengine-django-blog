"""
Functional tests that go through the full request response cycle.
They test HTML templates, middlewares and views.
"""
from ndbtestcase import AppEngineTestCase
from django.core.urlresolvers import reverse

from core.models import Blog, Article


def create_blog(**kwargs):
    """
    Helper function to create a blog in tests
    """
    default_kwargs = {
        'title': 'blog_title',
        'tagline': 'blog_tagline'
    }
    default_kwargs.update(kwargs)
    return Blog(key_name='blog', **default_kwargs).put()


class TestIndexPage(AppEngineTestCase):
    url = reverse('index')

    def setUp(self):
        create_blog()

    def test_name_and_tagline_in_page(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, 'blog_title')
        self.assertContains(resp, 'blog_tagline')

    def test_no_articles(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, 'This blog looks empty!')

    def test_articles_title_in_page(self):
        Article(title='title_article_one', body='body_one').put()
        Article(title='title_article_two',  body='body_two').put()
        resp = self.client.get(self.url)
        self.assertContains(resp, 'title_article_one')
        self.assertContains(resp, 'title_article_two')

    def test_articles_body_in_page(self):
        Article(title='title_article_one', body='body_one').put()
        Article(title='title_article_two',  body='body_two').put()
        resp = self.client.get(self.url)
        self.assertContains(resp, 'body_one')
        self.assertContains(resp, 'body_two')

    def test_visible_menu_when_admin(self):
        self.users_login('admin@localhost', is_admin=True)
        resp = self.client.get(self.url)
        self.assertContains(resp, 'Index')
        self.assertContains(resp, 'Settings')
        self.assertContains(resp, 'Add article')
        self.assertContains(resp, 'Logout')
        self.assertNotContains(resp, 'Login')

    def test_visible_menu_when_not_admin(self):
        self.users_login('user@localhost', is_admin=False)
        resp = self.client.get(self.url)
        self.assertContains(resp, 'Index')
        self.assertContains(resp, 'Logout')
        self.assertNotContains(resp, 'Login')
        self.assertNotContains(resp, 'Settings')
        self.assertNotContains(resp, 'Add article')

    def test_visible_menu_when_not_authenticated(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, 'Index')
        self.assertContains(resp, 'Login')
        self.assertNotContains(resp, 'Settings')
        self.assertNotContains(resp, 'Add article')
        self.assertNotContains(resp, 'Logout')


class TestArticleCreatePage(AppEngineTestCase):
    url = reverse('article_admin_create')

    def setUp(self):
        create_blog()

    def test_user_not_admin(self):
        self.users_login('user@localhost', is_admin=False)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_user_not_authenticated(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

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

        self.client.post(self.url, data)

        self.assertEqual(Article.all().count(), 0)

    def test_post_invalid_missing_title(self):
        self.users_login('admin@localhost', is_admin=True)
        data = {'body': 'article_body'}

        self.client.post(self.url, data)

        self.assertEqual(Article.all().count(), 0)


class TestUpdateBlog(AppEngineTestCase):
    url = reverse('blog_admin_update')

    def setUp(self):
        create_blog()

    def test_user_not_admin(self):
        self.users_login('user@localhost', is_admin=False)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_user_not_authenticated(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_post_no_title(self):
        self.users_login('admin@localhost', is_admin=True)
        data = {'tagline': 'new_tagline'}

        self.client.post(self.url, data)

        self.assertEqual(Blog.get_unique().title, 'blog_title')
        self.assertEqual(Blog.get_unique().tagline, 'blog_tagline')

    def test_post_valid(self):
        self.users_login('admin@localhost', is_admin=True)
        data = {'title': 'new_blog_title', 'tagline': 'new_tagline'}

        resp = self.client.post(self.url, data)

        blog = Blog.get_unique()
        self.assertRedirects(resp, reverse('index'))
        self.assertEqual(blog.title, 'new_blog_title')
        self.assertEqual(blog.tagline, 'new_tagline')


class TestDeleteArticle(AppEngineTestCase):
    def setUp(self):
        create_blog()

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

        self.assertRedirects(resp, reverse('index'))
        self.assertEqual(Article.all().count(), 0)


class TestUpdateArticle(AppEngineTestCase):
    def setUp(self):
        create_blog()
        self.key = Article(title='title123', body='body123').put()
        self.url = reverse(
            'article_admin_update',
            kwargs={'id': self.key.id()}
        )

    def test_user_not_admin(self):
        self.users_login('user@localhost', is_admin=False)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_user_not_authenticated(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_form_contains_article_title_and_body(self):
        self.users_login('admin@localhost', is_admin=True)
        resp = self.client.get(self.url)
        self.assertContains(resp, 'title123')
        self.assertContains(resp, 'body123')

    def test_post_no_body(self):
        self.users_login('admin@localhost', is_admin=True)
        data = {'title': 'new_title'}

        self.client.post(self.url, data)

        article = Article.get(self.key)
        self.assertEqual(article.title, 'title123')
        self.assertEqual(article.body, 'body123')

    def test_post_no_title(self):
        self.users_login('admin@localhost', is_admin=True)
        data = {'body': 'new_body'}

        self.client.post(self.url, data)

        article = Article.get(self.key)
        self.assertEqual(article.title, 'title123')
        self.assertEqual(article.body, 'body123')

    def test_post_valid(self):
        self.users_login('admin@localhost', is_admin=True)
        data = {'body': 'new_body', 'title': 'new_title'}

        self.client.post(self.url, data)

        article = Article.get(self.key)
        self.assertEqual(article.title, 'new_title')
        self.assertEqual(article.body, 'new_body')
