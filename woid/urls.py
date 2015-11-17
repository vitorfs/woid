# coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = patterns('',
    url(r'^$', 'woid.apps.services.views.front_page', name='front_page'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', { 'next_page': '/' }, name='logout'),
    url(r'^signup/', CreateView.as_view(template_name='registration/signup.html', form_class=UserCreationForm, success_url='/'), name='signup'),
    url(r'^about/', TemplateView.as_view(template_name='core/about.html'), name='about'),
    url(r'^status/', 'woid.apps.core.views.status', name='status'),
    url(r'^cookies/', TemplateView.as_view(template_name='core/cookies.html'), name='cookies'),
    url(r'^privacy/', TemplateView.as_view(template_name='core/privacy.html'), name='privacy'),
    url(r'^terms/', TemplateView.as_view(template_name='core/terms.html'), name='terms'),
    url(r'^(?P<slug>[-_\w]+)/', include('woid.apps.services.urls', namespace='services')),
    url(r'^admin/', include(admin.site.urls)),
)
