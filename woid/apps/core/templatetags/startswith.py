# coding: utf-8

from django import template

register = template.Library()


@register.filter('startswith')
def startswith(text, starts):
    starts = '/%s/' % starts
    if isinstance(text, str):
        return text.startswith(starts)
    return False
