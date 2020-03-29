==================
django-micro-press
==================

.. image:: https://travis-ci.com/jbradberry/django-micro-press.svg?branch=master
    :target: https://travis-ci.com/jbradberry/django-micro-press

django-micro-press is a pluggable app, intended to be embedded as a
simple newspaper in a game or other resource on a website.


Requirements
------------
- Python 2.7, 3.5+
- Django >= 1.10, < 2.3
- template-utils (`https://bitbucket.org/ubernostrum/django-template-utils`)
- lxml
- jsonfield


Installation
------------

Use pip to install django-micro-press from github
::

   pip install git+https://github.com/jbradberry/django-micro-press.git


or from your local development copy
::

   pip install -e django-micro-press/


Configuration
-------------

Add micropress to the ``INSTALLED_APPS`` list in your settings file.
::

   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',

       # Added.
       'micropress',
   ]

django-micro-press is intended to provide urls that attach to the url
scheme of your app or apps.  One way to do this is,
::

   from django.conf.urls import include, url

   urlpatterns = [
       url(r'^admin/', include('admin.site.urls')),
       url(r'^accounts/', include('django.contrib.auth.urls'),

       url(r'^my-game-app/', include('my_game_app.urls')),
       url(r'^my-game-app/(?P<realm_slug>[\w-]+)/news/',
           include('micropress.urls', namespace='my_game_app'),
           {'realm_content_type': 'my_game_app.game'}),
   ]


In order for the micropress views to function, they need to be aware
of the type of object they are pointing to (usually some kind of game
model).  This can be passed in to the url pattern as
``'realm_content_type'``, or if there is only one a given deployment
will ever use, it can be set as ``settings.DEFAULT_REALM_TYPE``.
These views then support using either a primary key (by default,
``realm_pk``) or a unique string (``realm_slug``) as an identifier.
Provide a named pattern in the url pattern for one of these, depending
on which the urls for your app use for its url scheme.
