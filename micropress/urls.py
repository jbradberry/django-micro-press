from django.conf.urls.defaults import *


urlpatterns = patterns('micropress.views',
    url(r'^$', 'article_list', name='press_article_list'),
    url(r'^issue/(?P<issue>\d+)/$', 'article_list', name='issue_list'),
    (r'^article/(?P<slug>[-\w]+)/$', 'article_detail'),
    #(r'^new/$', 'article_create'),
)
