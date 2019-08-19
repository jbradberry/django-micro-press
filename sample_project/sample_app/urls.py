from django.conf.urls import patterns, include, url

from .views import RealmView


urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)', RealmView.as_view()),
)
