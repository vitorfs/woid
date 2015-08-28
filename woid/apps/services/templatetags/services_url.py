# coding: utf-8

from django import template
from django.utils import timezone
from django.utils.html import escape
from django.core.urlresolvers import reverse as r

register = template.Library()


@register.simple_tag
def services_url(slug, delta):
    today = timezone.now()
    date = today - timezone.timedelta(delta)
    return r('services:day', args=(slug, date.year, str(date.month).zfill(2), str(date.day).zfill(2),))

@register.simple_tag
def services_url_name(slug, delta):
    today = timezone.now()
    date = today - timezone.timedelta(delta)
    return date.strftime('%A').lower()
