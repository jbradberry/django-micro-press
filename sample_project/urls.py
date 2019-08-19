from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^app/', include('sample_project.sample_app.urls')),
    url(r'^app/(?P<realm_slug>[\w-]+)/news/', include('micropress.urls'),
        {'realm_content_type': 'sample_app.testrealm'}),
    url(r'^accounts/', include('django.contrib.auth.urls')),
)
