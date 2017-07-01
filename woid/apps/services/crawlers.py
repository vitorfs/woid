# coding: utf-8

import logging

from django.utils import timezone

from woid.apps.services.models import Service, Story, StoryUpdate
from woid.apps.services import wrappers


class AbstractBaseCrawler(object):
    def __init__(self, slug, client):
        self.service = Service.objects.get(slug=slug)
        self.slug = slug
        self.client = client

    def run(self):
        try:
            self.service.status = Service.CRAWLING
            self.service.last_run = timezone.now()
            self.service.save()
            self.update_top_stories()
            self.service.status = Service.GOOD
            self.service.save()
        except:
            try:
                service = Service.objects.get(slug=self.slug)
                service.status = Service.ERROR
                service.save()
            except:
                pass

class HackerNewsCrawler(AbstractBaseCrawler):
    def __init__(self):
        super(HackerNewsCrawler, self).__init__('hn', wrappers.HackerNewsClient())

    def update_top_stories(self):
        try:
            stories = self.client.get_top_stories()
            i = 1
            for code in stories:
                self.update_story(code)
                i += 1
                if i > 100:
                    break
        except Exception, e:
            logging.error(e)

    def update_story(self, code):
        try:
            story_data = self.client.get_story(code)
            if story_data and story_data['type'] == 'story':
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

                '''
                if not story.status == Story.NEW and has_changes:
                    update = StoryUpdate(story=story)
                    update.comments_changes = comments - story.comments
                    update.score_changes = score - story.score
                    update.save()
                '''
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


class RedditCrawler(AbstractBaseCrawler):
    def __init__(self):
        super(RedditCrawler, self).__init__('reddit', wrappers.RedditClient())

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

                '''
                if not story.status == Story.NEW and has_changes:
                    update = StoryUpdate(story=story)
                    update.comments_changes = comments - story.comments
                    update.score_changes = score - story.score
                    update.save()
                '''

                story.comments = comments
                story.score = score
                story.title = story_data.get('title', '')
                story.nsfw = story_data.get('over_18', False)

                story.status = Story.OK
                story.save()
        except Exception, e:
            logging.error(e)


class GithubCrawler(AbstractBaseCrawler):
    def __init__(self):
        super(GithubCrawler, self).__init__('github', wrappers.GithubClient())

    def update_top_stories(self):
        try:
            repos = self.client.get_today_trending_repositories()
            today = timezone.now()
            for data in repos:
                story, created = Story.objects.get_or_create(service=self.service, code=data.get('name'), date=timezone.datetime(today.year, today.month, today.day, tzinfo=timezone.get_current_timezone()))
                if created:
                    story.build_url()

                stars = data.get('stars', 0)
                '''
                    Because of the nature of the github trending repositories
                    we are only interested on changes where the stars have increased
                    this way the crawler is gonna campure the highest starts one repository
                    got in a single day
                '''
                has_changes = (stars > story.score)

                if story.status == Story.NEW:
                    story.score = stars
                elif has_changes:
                    '''
                    update = StoryUpdate(story=story)
                    update.score_changes = stars - story.score
                    update.save()
                    '''
                    story.score = stars

                story.title = data.get('name')[1:]

                description = data.get('description', '')
                language = data.get('language', '')

                if language and description:
                    description = u'{0} • {1}'.format(language, description)
                elif language:
                    description = language

                story.description = description

                story.status = Story.OK
                story.save()

        except Exception, e:
            logging.error(e)


class MediumCrawler(AbstractBaseCrawler):
    def __init__(self):
        super(MediumCrawler, self).__init__('medium', wrappers.MediumClient())

    def update_top_stories(self):
        try:
            posts = self.client.get_top_stories()
            today = timezone.now()
            for post_data in posts:
                story, created = Story.objects.get_or_create(service=self.service, code=post_data['id'], date=timezone.datetime(today.year, today.month, today.day, tzinfo=timezone.get_current_timezone()))

                if created:
                    story.url = u'{0}/@{1}/{2}'.format(self.service.story_url, post_data['creator']['username'], post_data['id'])
                    story.start_score = int(post_data['virtuals']['recommends'])
                    story.start_comments = int(post_data['virtuals']['responsesCreatedCount'])

                story.title = post_data['title']

                recommends = int(post_data['virtuals']['recommends']) - story.start_score
                comments = int(post_data['virtuals']['responsesCreatedCount']) - story.start_comments
                has_changes = (recommends != story.score or comments != story.comments)

                '''
                if not story.status == Story.NEW and has_changes:
                    update = StoryUpdate(story=story)
                    update.comments_changes = comments - story.comments
                    update.score_changes = recommends - story.score
                    update.save()
                '''

                story.score = recommends
                story.comments = comments

                story.status = Story.OK
                story.save()

        except Exception, e:
            logging.error(e)


class NyTimesCrawler(AbstractBaseCrawler):
    def __init__(self):
        super(NyTimesCrawler, self).__init__('nytimes', wrappers.NyTimesClient())

    def save_story(self, story_data, score, weight):
        story_id = story_data.get('id', story_data.get('asset_id', None))
        if not story_id:
            return

        today = timezone.now()
        story, created = Story.objects.get_or_create(
                service=self.service,
                code=story_id,
                date=timezone.datetime(today.year, today.month, today.day, tzinfo=timezone.get_current_timezone())
            )

        story.title = story_data['title']
        story.url = story_data['url']

        minutes_since_last_update = 0

        if story.updates.exists():
            last_update = story.updates.order_by('-updated_at').first()
            delta = timezone.now() - last_update.updated_at
            minutes_since_last_update = delta.total_seconds() / 60

        if created or minutes_since_last_update >= 30:
            score_run = score * weight
            story.score += score_run

            update = StoryUpdate(story=story)
            update.score_changes = score_run
            update.save()

        story.status = Story.OK
        story.save()

    def update_top_stories(self):
        try:
            popular_stories = self.client.get_most_popular_stories()
            today = timezone.now()

            score = 20
            for story_data in popular_stories['mostviewed']:
                self.save_story(story_data, score, 4)
                score -= 1

            score = 20
            for story_data in popular_stories['mostshared']:
                self.save_story(story_data, score, 2)
                score -= 1

            score = 20
            for story_data in popular_stories['mostemailed']:
                self.save_story(story_data, score, 1)
                score -= 1

        except Exception, e:
            logging.error(e)


class DiggCrawler(AbstractBaseCrawler):
    def __init__(self):
        super(DiggCrawler, self).__init__('digg', wrappers.DiggClient())

    def update_top_stories(self):
        try:
            popular_stories = self.client.get_top_stories()
            today = timezone.now()

            for story_data in popular_stories:
                story, created = Story.objects.get_or_create(
                        service=self.service,
                        code=story_data['id'],
                        date=timezone.datetime(today.year, today.month, today.day, tzinfo=timezone.get_current_timezone())
                    )

                score = story_data['score']
                has_changes = (score > story.score)
                if not story.status == Story.NEW and has_changes:
                    update = StoryUpdate(story=story)
                    update.score_changes = score - story.score
                    update.save()

                story.title = story_data['title']
                story.url = story_data['url']
                story.score = score
                story.status = Story.OK
                story.save()

        except Exception, e:
            logging.error(e)
