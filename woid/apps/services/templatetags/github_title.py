# coding: utf-8

from django import template
from django.utils.html import escape

register = template.Library()


@register.filter('github_title')
def github_title(title):
    if title:
        repo = title.split('/')
        if len(repo) == 2:
            return '{0}/<strong>{1}</strong>'.format(escape(repo[0]), escape(repo[1]))
    return title
