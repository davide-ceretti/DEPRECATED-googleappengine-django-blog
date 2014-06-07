"""
Unit test models methods and properties.
"""
from django.http import Http404

from ndbtestcase import AppEngineTestCase
from core.models import Blog, Article


class TestBlog(AppEngineTestCase):
    def test_get_unique_no_blogs(self):
        blog = Blog.get_unique()
        self.assertEqual(blog.key().name(), 'blog')
        self.assertEqual(blog.title, 'My Blog')
        self.assertEqual(blog.tagline, None)
        self.assertEqual(Blog.all().count(), 1)

    def test_get_unique_one_blog(self):
        blog = Blog(key_name='blog', title='blog_one')
        blog.put()

        result = Blog.get_unique()

        self.assertEqual(result.title, 'blog_one')
        self.assertEqual(result.tagline, None)
        self.assertEqual(Blog.all().count(), 1)


class TestArticle(AppEngineTestCase):
    def test_get_by_id_or_404_id_is_none(self):
        with self.assertRaises(Http404):
            Article.get_by_id_or_404(None)

    def test_get_by_id_or_404_no_article(self):
        key = Article(title='title', body='body').put()
        free_key = key.id() + 1
        with self.assertRaises(Http404):
            Article.get_by_id_or_404(free_key)

    def test_get_by_id_or_404_article_found(self):
        key = Article(title='title', body='body').put()
        result = Article.get_by_id_or_404(key.id())
        self.assertEqual(key, result.key())
