# coding: utf-8

from django.db import models


class Service(models.Model):
    GOOD = 'G'
    ERROR = 'E'
    CRAWLING = 'C'
    CURRENT_STATUS = (
        (GOOD, '✓ good'),
        (ERROR, '× error'),
        (CRAWLING, '~ running')
        )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)
    url = models.URLField()
    story_url = models.URLField()
    last_run = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, default=GOOD, choices=CURRENT_STATUS)

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'slug': self.slug,
            'url': self.url
        }

    def get_story_template(self):
        template = 'services/includes/{0}_story.html'.format(self.slug)
        return template


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

    service = models.ForeignKey(Service, related_name='stories', on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=500, null=True, blank=True)
    url = models.URLField(max_length=2000, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    content_type = models.CharField(max_length=1, choices=CONTENT_TYPES, null=True, blank=True)
    start_comments = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    start_score = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True, db_index=True)
    status = models.CharField(max_length=1, default=NEW, choices=STATUS)
    top_ten = models.BooleanField(default=False)
    nsfw = models.BooleanField(default=False)
    description = models.CharField(max_length=2000, null=True, blank=True)

    class Meta:
        verbose_name = 'story'
        verbose_name_plural = 'stories'
        unique_together = (('service', 'code', 'date'),)
        ordering = ('-score',)

    def __str__(self):
        return self.code

    def build_url(self):
        self.url = '{0}{1}'.format(self.service.story_url, self.code)
        return self.url

    def get_template(self):
        return self.service.get_story_template()

    def to_dict(self):
        return {
            'code': self.code,
            'title': self.title,
            'url': self.url,
            'comments': self.comments,
            'score': self.score,
            'description': self.description
        }


class StoryUpdate(models.Model):
    story = models.ForeignKey(Story, related_name='updates', on_delete=models.CASCADE)
    comments_changes = models.IntegerField(default=0)
    score_changes = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'services_story_update'
        verbose_name = 'story update'
        verbose_name_plural = 'stories updates'

    def __str__(self):
        return self.story.code
