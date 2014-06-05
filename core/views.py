from django.views.generic import ListView, FormView, View, DeleteView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from google.appengine.api import users

from core.models import Article, Blog
from core.forms import ArticleForm, BlogForm


class BlogMixin(object):
    """
    Basic mixin for all the views. Update the context with additional
    information that is required across the whole site, typically
    to render base.html properly
    """
    def get_context_data(self, *args, **kwargs):
        context = super(BlogMixin, self).get_context_data(*args, **kwargs)
        blog = Blog.get_unique()
        context.update({
            'blog': blog,
            'active_user': users.get_current_user(),
            'is_admin': users.is_current_user_admin()
        })
        return context


class AdminRequiredMixin(object):
    """
    Mixin that redirects to the login page if users are not
    authenticated or they are not administrators
    """
    def get_after_login_url(self):
        raise NotImplementedError

    def dispatch(self, request, *args, **kwargs):
        if not users.is_current_user_admin():
            url = users.create_login_url(self.get_after_login_url())
            return HttpResponseRedirect(url)
        return super(AdminRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class LoginView(View):
    """
    A simple login page that uses Google App Engine authentication
    """
    def get(self, request):
        index = reverse('index')
        url = users.create_login_url(index)
        return HttpResponseRedirect(url)


class LogoutView(View):
    """
    A simple logout page that uses Google App Engine authentication
    """
    def get(self, request):
        index = reverse('index')
        url = users.create_logout_url(index)
        return HttpResponseRedirect(url)


class IndexView(BlogMixin, ListView):
    """
    The index page of the site. Contains the body and the titles of
    all the articles.
    """
    template_name = 'index.html'
    queryset = Article.all()


class ArticleAdminListView(AdminRequiredMixin, BlogMixin, ListView):
    """
    Administration page to view, update, delete articles.
    """
    template_name = 'article_admin_list.html'
    queryset = Article.all()

    def get_after_login_url(self):
        return reverse('article_admin_list')


class ArticleAdminCreateView(AdminRequiredMixin, BlogMixin, FormView):
    """
    Administration page to create articles.
    """
    template_name = 'form.html'
    form_class = ArticleForm

    def get_after_login_url(self):
        return reverse('article_admin_create')

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        self.form_class.create_article(data=form.cleaned_data)
        return super(ArticleAdminCreateView, self).form_valid(form)


class BlogAdminUpdateView(AdminRequiredMixin, BlogMixin, FormView):
    """
    Administration page to update blog settings.
    """
    template_name = 'form.html'
    form_class = BlogForm

    def get_after_login_url(self):
        return reverse('blog_admin_update')

    def get_success_url(self):
        return reverse('index')

    def get_initial(self):
        return {'title': self.get_object().title}

    def get_object(self):
        return Blog.get_unique()

    def form_valid(self, form):
        blog = self.get_object()
        self.form_class.update_blog(blog, data=form.cleaned_data)
        return super(BlogAdminUpdateView, self).form_valid(form)


class ArticleAdminDeleteView(AdminRequiredMixin, BlogMixin, DeleteView):
    """
    Delete the article with a given key
    """

    def get_after_login_url(self):
        return reverse('article_admin_list')

    def get_success_url(self):
        return reverse('article_admin_list')

    def get_object(self):
        obj_id = self.kwargs.get('id', None)
        return Article.get_by_id_or_404(obj_id)

    def get(self, request, *args, **kwargs):
        # For simplicity we delete on get requests
        return self.delete(request, *args, **kwargs)


class ArticleAdminUpdateView(AdminRequiredMixin, BlogMixin, FormView):
    """
    Administration page to update articles.
    """
    template_name = 'form.html'
    form_class = ArticleForm

    def get_after_login_url(self):
        return reverse('article_admin_list')

    def get_success_url(self):
        return reverse('index')

    def get_object(self):
        obj_id = self.kwargs.get('id', None)
        return Article.get_by_id_or_404(obj_id)

    def get_initial(self):
        article = self.get_object()
        data = {
            'title': article.title,
            'body': article.body
        }
        return data

    def form_valid(self, form):
        article = self.get_object()
        self.form_class.update_article(article, data=form.cleaned_data)
        return super(ArticleAdminUpdateView, self).form_valid(form)
