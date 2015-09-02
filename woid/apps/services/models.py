# coding: utf-8

from django.db import models

from woid.apps.services.managers import ServiceManager, StoryManager


class Service(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    url = models.URLField()
    story_url = models.URLField()

    objects = ServiceManager()

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __unicode__(self):
        return self.name


class Story(models.Model):
    TEXT = 'T'
    URL = 'U'
    IMAGE = 'I'
    CONTENT_TYPES = (
        (TEXT, 'text'),
        (URL, 'url'),
        (IMAGE, 'image'),
    )

    NEW = 'N'
    OK = 'O'
    ERROR = 'E'
    STATUS = (
        (NEW, 'New'),
        (OK, 'Ok'),
        (ERROR, 'Error'),
    )

    service = models.ForeignKey(Service, related_name='stories')
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=500, null=True, blank=True)
    url = models.URLField(max_length=2000, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    content_type = models.CharField(max_length=1, choices=CONTENT_TYPES, null=True, blank=True)
    comments = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, default=NEW, choices=STATUS)
    top_ten = models.BooleanField(default=False)

    objects = StoryManager()

    class Meta:
        verbose_name = 'story'
        verbose_name_plural = 'stories'
        unique_together = (('service', 'code', 'date'),)
        ordering = ('-score',)

    def __unicode__(self):
        return self.code

    def build_url(self):
        self.url = u'{0}{1}'.format(self.service.story_url, self.code)
        return self.url

    def get_template(self):
        template = u'services/includes/{0}_story.html'.format(self.service.slug)
        return template


class StoryUpdate(models.Model):
    story = models.ForeignKey(Story, related_name='updates')
    comments_changes = models.IntegerField(default=0)
    score_changes = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'services_story_update'
        verbose_name = 'story update'
        verbose_name_plural = 'stories updates'

    def __unicode__(self):
        return self.story.code
