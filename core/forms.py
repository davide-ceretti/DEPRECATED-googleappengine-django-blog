from django import forms

from core.models import Article, Blog


class ArticleCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField()

    @staticmethod
    def create_article(data):
        title = data.get('title')
        body = data.get('body')
        Article(title=title, body=body).put()


class BlogUpdateForm(forms.Form):
    title = forms.CharField(max_length=100)

    @staticmethod
    def update_blog(data):
        title = data.get('title')
        blog = Blog.get_unique()
        blog.title = title
        blog.put()
