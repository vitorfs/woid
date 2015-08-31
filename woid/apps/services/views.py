# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from woid.apps.services.models import Service, Story


def stories(request, service, queryset, subtitle):
    paginator = Paginator(queryset, 100)
    page = request.GET.get('page')
    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        stories = paginator.page(1)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)

    if stories.number > 1:
        start = (stories.number - 1) * 100 + 1
    else:
        start = 1

    return render(request, 'services/stories.html', {
        'service': service,
        'stories': stories,
        'subtitle': subtitle,
        'start': start
    })

def index(request, slug):
    today = timezone.now()
    return day(request, slug, today.year, today.month, today.day)

def year(request, slug, year):
    service = get_object_or_404(Service, slug=slug)
    queryset = service.stories.filter(status=Story.OK, date__year=year)
    return stories(request, service, queryset, year)

def month(request, slug, year, month):
    service = get_object_or_404(Service, slug=slug)
    queryset = service.stories.filter(status=Story.OK, date__year=year, date__month=month)
    subtitle = timezone.datetime(int(year), int(month), 1).strftime('%b %Y')
    return stories(request, service, queryset, subtitle)

def day(request, slug, year, month, day):
    service = get_object_or_404(Service, slug=slug)
    queryset = service.stories.filter(status=Story.OK, date__year=year, date__month=month, date__day=day)
    subtitle = timezone.datetime(int(year), int(month), int(day)).strftime('%d %b %Y')
    return stories(request, service, queryset, subtitle)

def archive(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'services/archive.html', {
        'service': service
    })
