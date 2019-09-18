from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^one/', include('sample_project.app_one.urls')),
    url(r'^one/(?P<realm_slug>[\w-]+)/news/',
        include('micropress.urls', namespace='app_one'),
        {'realm_content_type': 'app_one.onegame'}),
    url(r'^two/', include('sample_project.app_one.urls')),
    url(r'^two/games/(?P<realm_slug>[\w-]+)/news/',
        include('micropress.urls', namespace='app_two'),
        {'realm_content_type': 'app_two.twogame'}),
    url(r'^two/also/(?P<realm_slug>[\w-]+)/news/',
        include('micropress.urls', namespace='app_two_also'),
        {'realm_content_type': 'app_two.twogamealso'}),
)
