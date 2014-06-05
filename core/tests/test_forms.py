"""
Unit test forms methods and properties.
"""
from ndbtestcase import AppEngineTestCase

from core.models import Article, Blog
from core.forms import ArticleForm, BlogForm


class TestArticleForm(AppEngineTestCase):
    def test_create_article(self):
        data = {
            'title': 'article_title',
            'body': 'article_body'
        }

        ArticleForm.create_article(data)

        self.assertEqual(Article.all().count(), 1)


class TestBlogForm(AppEngineTestCase):
    def test_update_blog(self):
        blog = Blog(title='old_title')
        key = blog.put()
        data = {
            'title': 'new_title',
        }

        BlogForm.update_blog(blog, data)

        blog = Blog.get(key)
        self.assertEqual(blog.title, 'new_title')
