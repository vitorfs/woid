# coding: utf-8

from django import template
from django.urls import reverse as r
from django.utils import timezone

register = template.Library()


@register.simple_tag
def services_url(slug, delta):
    today = timezone.now()
    date = today - timezone.timedelta(delta)
    return r('services:day', args=(slug, date.year, str(date.month).zfill(2), str(date.day).zfill(2),))


@register.simple_tag
def services_url_month(slug):
    date = timezone.now()
    return r('services:month', args=(slug, date.year, str(date.month).zfill(2),))


@register.simple_tag
def services_url_year(slug):
    date = timezone.now()
    return r('services:year', args=(slug, date.year,))


@register.simple_tag
def services_url_name(slug, delta):
    today = timezone.now()
    date = today - timezone.timedelta(delta)
    return date.strftime('%A').lower()


@register.simple_tag
def services_url_month_name():
    return timezone.now().strftime('%B').lower()
