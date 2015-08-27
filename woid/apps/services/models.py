# coding: utf-8

from django.db import models

from woid.apps.services.managers import ServiceManager, StoryManager


class Service(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    objects = ServiceManager()

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __unicode__(self):
        return self.name

    def get_today_stories(self):
        return self.stories.get_today_stories()

class Story(models.Model):
    service = models.ForeignKey(Service, related_name='stories')
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    comments = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    visited_at = models.DateTimeField(auto_now=True)

    objects = StoryManager()

    class Meta:
        verbose_name = 'story'
        verbose_name_plural = 'stories'
        unique_together = (('service', 'code'),)
        ordering = ('-score',)

    def __unicode__(self):
        return self.code
