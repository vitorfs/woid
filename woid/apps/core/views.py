# coding: utf-8

from django.contrib import messages
from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')
