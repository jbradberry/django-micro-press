from django.conf.urls.defaults import *


urlpatterns = patterns('micropress.views',
    url(r'^$', 'article_list', {'paginate_by': 25}, name='press_article_list'),
    url(r'^issue/(?P<issue>\d+)/$', 'article_list', name='issue_list'),
    url(r'^article/(?P<slug>[-\w]+)/$', 'article_detail', name='article_detail'),
    #(r'^new/$', 'article_create'),
)
