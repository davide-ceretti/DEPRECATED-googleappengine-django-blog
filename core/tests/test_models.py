"""
Unit test models methods and properties.
"""
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from ndbtestcase import AppEngineTestCase
from core.models import Blog


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
