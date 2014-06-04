from django.conf import settings
from django.conf.urls.defaults import url, patterns

from core import views


urlpatterns = patterns(
    'core.views',
    url(r'^$', views.ArticleListView.as_view(), name='article_list'),
    url(r'^add/$', views.ArticleCreateView.as_view(), name='article_create'),
)


if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.generic.simple',
        url(r'^500/$', 'direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'direct_to_template', {'template': '404.html'}),
    )
