from django.views.generic import ListView

from core.models import Article, Blog


class BlogMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BlogMixin, self).get_context_data(*args, **kwargs)
        blog = Blog.all()[0]
        context.update({
            'blog': blog,
        })
        return context


class ArticleListView(BlogMixin, ListView):
    template_name = 'article_list.html'
    queryset = Article.all()
