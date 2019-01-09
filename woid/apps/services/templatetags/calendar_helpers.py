# coding: utf-8

import calendar

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


def get_calendar(year, month):
    blank_week = [0, 0, 0, 0, 0, 0, 0]
    calendar.setfirstweekday(calendar.SUNDAY)
    c = calendar.monthcalendar(year, month)
    if len(c) == 4:
        c.append(blank_week)
    if len(c) == 5:
        c.append(blank_week)
    return c


@register.simple_tag
def month_calendar(year, month, days, service):
    calendar.setfirstweekday(calendar.SUNDAY)
    month_calendar = calendar.monthcalendar(int(year), int(month))

    month_name = calendar.month_name[int(month)]
    month_href = reverse('services:month', args=(service.slug, year, month))

    html = '<table><thead>'
    html += '<tr><th colspan="7"><a href="{0}">{1}</a></th></tr>'.format(month_href, month_name)
    html += '<tr><th>s</th><th>m</th><th>t</th><th>w</th><th>t</th><th>f</th><th>s</th></tr>'
    html += '</thead><tbody>'
    for week in month_calendar:
        html += '<tr>'
        for day in week:
            if day == 0:
                str_day = ''
            else:
                str_day = str(day).zfill(2)
            if str_day in days:
                day_href = reverse('services:day', args=(service.slug, year, month, str_day))
                html += '<td><a href="{0}">{1}</a></td>'.format(day_href, str_day)
            else:
                html += '<td>{0}</td>'.format(str_day)
        html += '</tr>'
    html += '</tbody></table>'
    return mark_safe(html)


@register.filter('month_name')
def month_name(month):
    names = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }
    return names[month]
