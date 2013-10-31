from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='issue/current/', permanent=False)),
    url(r'^article/$', RedirectView.as_view(url='../issue/current/',
                                            permanent=False)),
    url(r'^article/(?P<slug>[-\w]+)/$', views.ArticleDetailView.as_view(),
        name='article_detail'),
    url(r'^issue/$', views.IssueListView.as_view(),
        name='issue_list'),
    url(r'^issue/(?P<issue>[\d\w]+)/$', views.ArticleListView.as_view(),
        name='article_list'),
    url(r'^post/$', views.ArticleCreateView.as_view(), name='article_create'),
)
