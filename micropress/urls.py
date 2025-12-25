from django.views.generic import RedirectView
from django.urls import re_path

from . import views


app_name = 'micropress'
urlpatterns = [
    re_path(r'^$', RedirectView.as_view(url='article/', permanent=False)),
    re_path(r'^article/$', views.ArticleListView.as_view(), name='article_list'),
    re_path(r'^article/(?P<slug>[-\w]+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
    re_path(r'^post/$', views.ArticleCreateView.as_view(), name='article_create'),
]
