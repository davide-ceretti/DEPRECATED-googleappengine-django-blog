"""
Unit test models methods and properties.
"""
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404

from ndbtestcase import AppEngineTestCase
from core.models import Blog, Article


class TestBlog(AppEngineTestCase):
    def test_get_unique_no_blogs(self):
        with self.assertRaises(ObjectDoesNotExist):
            Blog.get_unique()

    def test_get_unique_multiple_blogs(self):
        Blog(title="blog_one").put()
        Blog(title="blog_two").put()
        with self.assertRaises(MultipleObjectsReturned):
            Blog.get_unique()

    def test_get_unique_one_blog(self):
        blog = Blog(title="blog_one")
        blog.put()

        result = Blog.get_unique()

        # TODO: Implement self.assertObjectEqual()
        self.assertEqual(result.key(), blog.key())


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
