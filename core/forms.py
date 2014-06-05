from django import forms
from core.models import Article


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)

    @staticmethod
    def create_article(data):
        title = data.get('title')
        body = data.get('body')
        Article(title=title, body=body).put()

    @staticmethod
    def update_article(article, data):
        article.body = data.get('body')
        article.title = data.get('title')
        article.put()


class BlogForm(forms.Form):
    title = forms.CharField(max_length=100)

    @staticmethod
    def update_blog(blog, data):
        title = data.get('title')
        blog.title = title
        blog.put()
