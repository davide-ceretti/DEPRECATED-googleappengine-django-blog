from google.appengine.ext import db


class Blog(db.Model):
    title = db.StringProperty(required=True)


class Article(db.Model):
    title = db.StringProperty(required=True)
