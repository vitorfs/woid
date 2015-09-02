# coding: utf-8

from collections import OrderedDict
from itertools import groupby

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

def all(request):
    today = timezone.now()
    queryset = Story.objects.filter(status=Story.OK, date__year=today.year, date__month=today.month, date__day=today.day)[:10]
    subtitle = today.strftime('%d %b %Y')
    return render(request, 'services/all.html', { 'stories': stories, 'subtitle': subtitle })

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

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def archive(request, slug):
    service = get_object_or_404(Service, slug=slug)

    dates = service.stories.all().order_by('-date').values_list('date', flat=True)
    str_dates = map(lambda date: date.strftime('%Y-%m-%d'), dates)
    str_dates = remove_duplicates(str_dates)

    archive = OrderedDict()
    for year, months in groupby(str_dates, lambda date: date[:4]):
        archive[year] = OrderedDict()
        for month, days in groupby(months, lambda date: date[5:7]):
            archive[year][month] = list()
            for day in days:
                archive[year][month].append(day[8:10])

    return render(request, 'services/archive.html', {
        'service': service,
        'archive': archive
    })
