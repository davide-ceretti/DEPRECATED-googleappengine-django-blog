from django import forms

from core.models import Article


class ArticleCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField()

    @staticmethod
    def create_article(data):
        title = data.get('title')
        body = data.get('body')
        Article(title=title, body=body).put()
