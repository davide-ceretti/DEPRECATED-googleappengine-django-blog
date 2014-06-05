from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404

from google.appengine.ext import db


class Blog(db.Model):
    title = db.StringProperty(required=True)
    tagline = db.StringProperty()

    @staticmethod
    def get_unique():
        """
        Returns the only instance of the Blog in the data store.
        If there are no Blog or there are more than one, raise an
        exception.
        """
        blogs = Blog.all()
        count = blogs.count()
        if count == 0:
            raise ObjectDoesNotExist
        elif count > 1:
            raise MultipleObjectsReturned
        return blogs[0]


class Article(db.Model):
    title = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def get_by_id_or_404(obj_id):
        """
        Get the article with the given ID, if it can't be found
        raise 404
        """
        if obj_id is None:
            raise Http404
        article = Article.get_by_id(int(obj_id))
        if article is None:
            raise Http404
        return article
