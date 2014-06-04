from django.views.generic import ListView, FormView
from django.core.urlresolvers import reverse

from core.models import Article, Blog
from core.forms import ArticleCreateForm


class BlogMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BlogMixin, self).get_context_data(*args, **kwargs)
        blog = Blog.get_unique()
        context.update({
            'blog': blog,
        })
        return context


class ArticleListView(BlogMixin, ListView):
    template_name = 'article_list.html'
    queryset = Article.all()


class ArticleCreateView(BlogMixin, FormView):
    template_name = 'article_create.html'
    form_class = ArticleCreateForm

    def get_success_url(self):
        return reverse('article_list')

    def form_valid(self, form):
        self.form_class.create_article(data=form.cleaned_data)
        return super(ArticleCreateView, self).form_valid(form)
