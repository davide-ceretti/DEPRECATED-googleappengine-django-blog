"""
NOTE: The google.appengine.ext.db.djangoforms module is not provided
with the Python 2.7. Therefore we forked their djangoforms
"""
from lib import djangoforms

from core.models import Article, Blog


class ArticleForm(djangoforms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body')


class BlogForm(djangoforms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title',)
