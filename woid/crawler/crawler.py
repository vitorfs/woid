# coding: utf-8

from datetime import datetime

from django.utils import timezone

from woid.apps.services.models import Service, Story
from woid.apps.services.wrappers import HackerNewsClient, RedditClient


class HackerNewsCrawler(object):
    def __init__(self):
        self.service = Service.objects.get(slug='hn')
        self.client = HackerNewsClient()

    def update_top_stories(self):
        stories = self.client.get_top_stories()
        for code in stories:
            Story.objects.get_or_create(service=self.service, code=code)

    def update_story(self, code):
        story_data = self.client.get_story(code)
        if story_data:
            story, created = Story.objects.get_or_create(service=self.service, code=code)
            story.comments = story_data.get('descendants', 0)
            story.score = story_data.get('score', 0)
            story.date = datetime.fromtimestamp(story_data.get('time'), timezone.get_current_timezone())
            story.title = story_data.get('title', '')
            story.url = story_data.get('url', '')
            if not created:
                pass
            story.save()
