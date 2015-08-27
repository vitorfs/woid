# coding: utf-8

from woid.apps.services.models import Service, Story
from woid.apps.services.wrappers import HackerNews


class HackerNewsCrawler(object):
    def __init__(self):
        self.service = Service.objects.get(slug='hn')
        self.client = HackerNews()

    def update_top_stories(self):
        stories = self.client.get_top_stories()
        for story in stories:
            Story.objects.get_or_create(service=self.service, code=story)
