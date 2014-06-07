from django.http import Http404

from google.appengine.ext import db


class Blog(db.Model):
    title = db.StringProperty(required=True)
    tagline = db.StringProperty()

    @staticmethod
    def get_unique():
        """
        Returns the only instance of the Blog in the data store.
        If there are no Blog it creates a default one.
        """
        blog = Blog.get_or_insert('blog', title='My Blog')
        return blog


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
