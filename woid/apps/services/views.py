# coding: utf-8

from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from woid.apps.services.models import Service, Story


def index(request, slug):
    today = timezone.now()
    return day(request, slug, today.year, today.month, today.day)

def archive(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'services/archive.html', {
        'service': service
    })

def year(request, slug, year):
    service = get_object_or_404(Service, slug=slug)
    stories = service.stories.filter(status=Story.OK, date__year=year)
    return render(request, 'services/stories.html', {
        'service': service,
        'stories': stories
    })

def month(request, slug, year, month):
    service = get_object_or_404(Service, slug=slug)
    stories = service.stories.filter(status=Story.OK, date__year=year, date__month=month)
    return render(request, 'services/stories.html', {
        'service': service,
        'stories': stories
    })

def day(request, slug, year, month, day):
    service = get_object_or_404(Service, slug=slug)
    stories = service.stories.filter(status=Story.OK, date__year=year, date__month=month, date__day=day)
    return render(request, 'services/stories.html', {
        'service': service,
        'stories': stories
    })
