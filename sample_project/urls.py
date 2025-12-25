from django.urls import include, re_path


urlpatterns = [
    re_path(r'^one/', include('sample_project.app_one.urls')),
    re_path(r'^one/(?P<realm_slug>[\w-]+)/news/', include('micropress.urls', namespace='app_one'),
            {'realm_content_type': 'app_one.onegame'}),
    re_path(r'^two/', include('sample_project.app_one.urls')),
    re_path(r'^two/games/(?P<realm_slug>[\w-]+)/news/', include('micropress.urls', namespace='app_two'),
            {'realm_content_type': 'app_two.twogame'}),
    re_path(r'^two/also/(?P<realm_slug>[\w-]+)/news/', include('micropress.urls', namespace='app_two_also'),
            {'realm_content_type': 'app_two.twogamealso'}),
]
