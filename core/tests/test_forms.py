"""
Unit test forms methods and properties.
"""
from ndbtestcase import AppEngineTestCase

from core.models import Article, Blog
from core.forms import ArticleCreateForm, BlogUpdateForm


class TestArticleCreateForm(AppEngineTestCase):
    def test_create_article(self):
        data = {
            'title': 'article_title',
            'body': 'article_body'
        }

        ArticleCreateForm.create_article(data)

        self.assertEqual(Article.all().count(), 1)


class TestBlogUpdateForm(AppEngineTestCase):
    def test_update_blog(self):
        Blog(title='old_title').put()
        data = {
            'title': 'new_title',
        }

        BlogUpdateForm.update_blog(data)

        blog = Blog.get_unique()
        self.assertEqual(blog.title, 'new_title')
