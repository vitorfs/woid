# coding: utf-8

from django.utils import timezone
from django.db import models


class ServiceManager(models.Manager):
    pass

class StoryManager(models.Manager):
    def get_today_stories(self):
        return self.get_queryset().filter(date=timezone.now())
