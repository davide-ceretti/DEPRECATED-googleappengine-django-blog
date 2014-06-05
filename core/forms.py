from google.appengine.ext.db import djangoforms

from core.models import Article, Blog


class ArticleForm(djangoforms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body')


class BlogForm(djangoforms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title',)
