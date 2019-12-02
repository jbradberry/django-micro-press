from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='article/', permanent=False)),
    url(r'^article/$', views.ArticleListView.as_view(),
        name='article_list'),
    url(r'^article/(?P<slug>[-\w]+)/$', views.ArticleDetailView.as_view(),
        name='article_detail'),
    url(r'^post/$', views.ArticleCreateView.as_view(), name='article_create'),
]
