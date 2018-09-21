from django.conf.urls import patterns, url


urlpatterns = patterns('woid.apps.feeds.views',
    url(r'^$', 'index', name='index'),
)
