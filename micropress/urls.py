from django.conf.urls.defaults import *


urlpatterns = patterns('micropress.views',
    (r'^$', 'article_list'),
    (r'^issue/(?P<issue>\d+)/$', 'issue_list'),
    (r'^article/(?P<slug>[-\w]+)/$', 'article_detail'),
    #(r'^new/$', 'article_create'),
)
