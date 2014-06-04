from ndbtestcase import AppEngineTestCase

from core.models import Blog


class TestArticleListPage(AppEngineTestCase):
    """
    Functional test for the article list page
    """
    def setUp(self):
        Blog(title="my_blog_title").put()
        self.resp = self.client.get('/')

    def test_correct_template_loaded(self):
        self.assertTemplateUsed(
            template_name="article_list.html",
            response=self.resp
        )

    def test_200_and_name_in_page(self):
        self.assertContains(self.resp, "my_blog_title")
