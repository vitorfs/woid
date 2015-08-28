# coding: utf-8

from django.conf.urls import patterns, include, url


urlpatterns = patterns('woid.apps.services.views',
    url(r'^$', 'index', name='index'),
    url(r'^archive/$', 'archive', name='archive'),
    url(r'^(?P<year>[0-9]{4})/$', 'year', name='year'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', 'month', name='month'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', 'day', name='day'),
)
