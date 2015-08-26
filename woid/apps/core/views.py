# coding: utf-8

from django.contrib import messages
from django.shortcuts import render


def home(request):
    messages.success(request, 'teste')
    messages.info(request, 'teste')
    messages.warning(request, 'teste')
    messages.error(request, 'teste')
    messages.debug(request, 'debug')
    return render(request, 'core/home.html')
