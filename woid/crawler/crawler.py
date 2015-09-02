# coding: utf-8

import logging

from django.utils import timezone

from woid.apps.services.models import Service, Story, StoryUpdate
from woid.apps.services.wrappers import HackerNewsClient, RedditClient


class HackerNewsCrawler(object):
    def __init__(self):
        self.service = Service.objects.get(slug='hn')
        self.client = HackerNewsClient()

    def index_all_stories(self, start=1, offset=1):
        try:
            max_item = self.client.get_max_item()
            i = start
            while i < max_item:
                self.update_story(i)
                i += offset
        except Exception, e:
            logging.error(e)

    def update_top_stories(self):
        try:
            stories = self.client.get_top_stories()
            for code in stories:
                Story.objects.get_or_create(service=self.service, code=code)
        except Exception, e:
            logging.error(e)

    def update_story(self, code):
        try:
            story_data = self.client.get_story(code)
            if story_data:
                story, created = Story.objects.get_or_create(service=self.service, code=code)

                if story_data.get('deleted', False):
                    story.delete()
                    return

                if story.status == Story.NEW:
                    story.date = timezone.datetime.fromtimestamp(story_data.get('time'), timezone.get_current_timezone())
                    story.url = u'{0}{1}'.format(story.service.story_url, story.code)
                
                score = story_data.get('score', 0)
                comments = story_data.get('descendants', 0)
                has_changes = (score != story.score or comments != story.comments)

                if not story.status == Story.NEW and has_changes:
                        update = StoryUpdate(story=story)
                        update.comments_changes = comments - story.comments
                        update.score_changes = score - story.score
                        update.save()

                story.comments = comments
                story.score = score
                story.title = story_data.get('title', '')

                url = story_data.get('url', '')
                if url:
                    story.content_type = Story.URL
                    story.content = url

                text = story_data.get('text', '')
                if text:
                    story.content_type = Story.TEXT
                    story.content = text

                story.status = Story.OK
                story.save()
        except Exception, e:
            logging.error(u'Exception in code {0} HackerNewsCrawler.update_story'.format(code))
            logging.error(e)


class RedditCrawler(object):
    def __init__(self):
        self.service = Service.objects.get(slug='reddit')
        self.client = RedditClient()

    def update_top_stories(self):
        try:
            stories = self.client.get_front_page_stories()
            for data in stories:
                story_data = data['data']
                story, created = Story.objects.get_or_create(service=self.service, code=story_data.get('permalink'))
                if created:
                    story.date = timezone.datetime.fromtimestamp(story_data.get('created_utc'), timezone.get_current_timezone())
                    story.build_url()

                score = story_data.get('score', 0)
                comments = story_data.get('num_comments', 0)
                has_changes = (score != story.score or comments != story.comments)

                if not story.status == Story.NEW and has_changes:
                        update = StoryUpdate(story=story)
                        update.comments_changes = comments - story.comments
                        update.score_changes = score - story.score
                        update.save()

                story.comments = comments
                story.score = score
                story.title = story_data.get('title', '')

                story.status = Story.OK
                story.save()
        except Exception, e:
            logging.error(e)
