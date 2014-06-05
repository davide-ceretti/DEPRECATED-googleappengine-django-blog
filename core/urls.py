from django.conf import settings
from django.conf.urls.defaults import url, patterns

from core import views


urlpatterns = patterns(
    'core.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LoginView.as_view(), name='logout'),
    url(r'^add/$', views.ArticleAdminCreateView.as_view(), name='article_admin_create'),
    url(r'^manage-articles/$', views.ArticleAdminListView.as_view(), name='article_admin_list'),
    url(r'^manage-blog/$', views.BlogAdminUpdateView.as_view(), name='blog_admin_update'),
    url(r'^delete-article/(?P<id>[\d]+)/$', views.ArticleAdminDeleteView.as_view(), name='article_admin_delete'),
    url(r'^update-article/(?P<id>[\d]+)/$', views.ArticleAdminUpdateView.as_view(), name='article_admin_update'),
)


if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.generic.simple',
        url(r'^500/$', 'direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'direct_to_template', {'template': '404.html'}),
    )
