from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from google.appengine.ext import db


class Blog(db.Model):
    title = db.StringProperty(required=True)

    @staticmethod
    def get_unique():
        # TODO: Optimize queries
        blogs = Blog.all()
        count = blogs.count()
        if count == 0:
            raise ObjectDoesNotExist
        elif count > 1:
            raise MultipleObjectsReturned
        return blogs[0]


class Article(db.Model):
    title = db.StringProperty(required=True)
