# coding: utf-8

import logging

from django.utils import timezone

from woid.apps.services import wrappers
from woid.apps.services.models import Service, Story, StoryUpdate

logger = logging.getLogger(__name__)


class AbstractBaseCrawler:
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
        except Exception:
            self.service.status = Service.ERROR
            self.service.save()


class HackerNewsCrawler(AbstractBaseCrawler):
    def __init__(self):
        super().__init__('hn', wrappers.HackerNewsClient())

    def update_top_stories(self):
        try:
            stories = self.client.get_top_stories()
            i = 1
            for code in stories:
                self.update_story(code)
                i += 1
                if i > 100:
                    break
        except Exception:
            logger.exception('An error occurred while executing `update_top_stores` for Hacker News.')
            raise

    def update_story(self, code):
        try:
            story_data = self.client.get_story(code)
            if story_data and story_data['type'] == 'story':
                story, created = Story.objects.get_or_create(service=self.service, code=code)

                if story_data.get('deleted', False):
                    story.delete()
                    return

                if story.status == Story.NEW:
                    story.date = timezone.datetime.fromtimestamp(
                        story_data.get('time'),
                        timezone.get_current_timezone()
                    )
                    story.url = u'{0}{1}'.format(story.service.story_url, story.code)

                score = story_data.get('score', 0)
                comments = story_data.get('descendants', 0)

                # has_changes = (score != story.score or comments != story.comments)

                # if not story.status == Story.NEW and has_changes:
                #     update = StoryUpdate(story=story)
                #     update.comments_changes = comments - story.comments
                #     update.score_changes = score - story.score
                #     update.save()

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
        except Exception:
            logger.exception('Exception in code {0} HackerNewsCrawler.update_story'.format(code))


class RedditCrawler(AbstractBaseCrawler):
    def __init__(self):
        super().__init__('reddit', wrappers.RedditClient())

    def update_top_stories(self):
        try:
            stories = self.client.get_front_page_stories()
            for data in stories:
                story_data = data['data']
                story, created = Story.objects.get_or_create(service=self.service, code=story_data.get('permalink'))
                if created:
                    story.date = timezone.datetime.fromtimestamp(
                        story_data.get('created_utc'),
                        timezone.get_current_timezone()
                    )
                    story.build_url()

                score = story_data.get('score', 0)
                comments = story_data.get('num_comments', 0)

                # has_changes = (score != story.score or comments != story.comments)

                # if not story.status == Story.NEW and has_changes:
                #     update = StoryUpdate(story=story)
                #     update.comments_changes = comments - story.comments
                #     update.score_changes = score - story.score
                #     update.save()

                story.comments = comments
                story.score = score
                story.title = story_data.get('title', '')
                story.nsfw = story_data.get('over_18', False)

                story.status = Story.OK
                story.save()
        except Exception:
            logger.exception('An error occurred while executing `update_top_stores` for Reddit.')
            raise


class GithubCrawler(AbstractBaseCrawler):
    def __init__(self):
        super().__init__('github', wrappers.GithubClient())

    def update_top_stories(self):
        try:
            repos = self.client.get_today_trending_repositories()
            today = timezone.now()
            for data in repos:
                story, created = Story.objects.get_or_create(
                    service=self.service,
                    code=data.get('name'),
                    date=timezone.datetime(today.year, today.month, today.day, tzinfo=timezone.get_current_timezone())
                )
                if created:
                    story.build_url()

                stars = data.get('stars', 0)

                # Because of the nature of the github trending repositories
                # we are only interested on changes where the stars have increased
                # this way the crawler is gonna campure the highest starts one repository
                # got in a single day
                has_changes = (stars > story.score)

                if story.status == Story.NEW:
                    story.score = stars
                elif has_changes:
                    # update = StoryUpdate(story=story)
                    # update.score_changes = stars - story.score
                    # update.save()
                    story.score = stars

                story.title = data.get('name')[1:]

                description = data.get('description', '')
                language = data.get('language', '')

                if language and description:
                    description = '{0} • {1}'.format(language, description)
                elif language:
                    description = language

                story.description = description

                story.status = Story.OK
                story.save()

        except Exception:
            logger.exception('An error occurred while executing `update_top_stores` for GitHub.')
            raise


class NYTimesCrawler(AbstractBaseCrawler):
    def __init__(self):
        super().__init__('nytimes', wrappers.NYTimesClient())

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

        except Exception:
            logger.exception('An error occurred while executing `update_top_stores` for NYTimes.')
            raise


class ProductHuntCrawler(AbstractBaseCrawler):
    def __init__(self):
        super().__init__('producthunt', wrappers.ProductHuntClient())

    def update_top_stories(self):
        try:
            posts = self.client.get_top_posts()
            today = timezone.now()
            for post in posts:
                code = post['slug']
                story, created = Story.objects.get_or_create(
                    service=self.service,
                    code=code,
                    date=timezone.datetime(today.year, today.month, today.day, tzinfo=timezone.get_current_timezone())
                )

                if created:
                    story.title = post['name']
                    story.description = post['tagline']
                    story.url = u'{0}{1}'.format(self.service.story_url, code)

                story.score = post['votes_count']
                story.comments = post['comments_count']
                story.status = Story.OK
                story.save()

        except Exception:
            logger.exception('An error occurred while executing `update_top_stores` for Product Hunt.')
            raise
