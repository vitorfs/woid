# coding: utf-8

from django import template

register = template.Library()


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, basestring):
        return text.startswith(starts)
    return False
