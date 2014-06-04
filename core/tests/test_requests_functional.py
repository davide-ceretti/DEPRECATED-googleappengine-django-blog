from ndbtestcase import AppEngineTestCase

from core.models import Blog, Article


class TestArticleListPage(AppEngineTestCase):
    """
    Functional test for the article list page
    """
    def setUp(self):
        Blog(title="my_blog_title").put()

    def test_correct_template_loaded(self):
        resp = self.client.get('/')
        self.assertTemplateUsed(
            template_name="article_list.html",
            response=resp
        )

    def test_200_and_name_in_page(self):
        resp = self.client.get('/')
        self.assertContains(resp, "my_blog_title")

    def test_no_articles(self):
        resp = self.client.get('/')
        self.assertContains(resp, "This blog looks empty!")

    def test_with_articles(self):
        Article(title="title_article_one").put()
        Article(title="title_article_two").put()
        resp = self.client.get('/')
        self.assertContains(resp, "title_article_one")
        self.assertContains(resp, "title_article_two")
