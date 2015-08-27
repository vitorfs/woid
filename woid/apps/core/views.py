# coding: utf-8

from django.contrib import messages
from django.shortcuts import render

from woid.apps.services.models import Service


def home(request):
    hacker_news = Service.objects.get(slug='hn')
    return render(request, 'core/home.html', {
        'hacker_news': hacker_news
    })
