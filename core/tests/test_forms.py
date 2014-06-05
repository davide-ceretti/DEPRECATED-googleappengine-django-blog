"""
Unit test forms methods and properties.
"""
from ndbtestcase import AppEngineTestCase

from core.models import Article
from core.forms import ArticleCreateForm


class TestArticleCreateForm(AppEngineTestCase):
    def test_create_article(self):
        data = {
            'title': 'article_title',
            'body': 'article_body'
        }

        ArticleCreateForm.create_article(data)

        self.assertEqual(Article.all().count(), 1)
