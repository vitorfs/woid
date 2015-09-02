from unipath import Path
import sys
import os

PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woid.settings')

import django
django.setup()


import time
import threading

from django.utils import timezone

from woid.crawler.crawler import HackerNewsCrawler
from woid.apps.services.models import Service, Story


FIVE_MINUTES = 5 * 60
TWELVE_HOURS = 12 * 60 * 60
HACKER_NEWS_SLUG = 'hackernews'


class HackerNewsService(threading.Thread):
    def __init__(self):
        super(HackerNewsService, self).__init__()
        self.crawler = HackerNewsCrawler()
        self.service = Service.objects.get(slug=HACKER_NEWS_SLUG)


class HNSUpdateTopStories(HackerNewsService):
    def run(self):
        run_count = 0
        while True:
            run_count = run_count + 1
            self.crawler.update_top_stories()
            time.sleep(FIVE_MINUTES)


class HNSUpdateTodayStoriesData(HackerNewsService):
    def run(self):
        run_count = 0
        while True:
            run_count = run_count + 1
            today = timezone.now()
            today_stories = self.service.stories \
                    .filter(date__year=today.year, date__month=today.month, date__day=today.day) \
                    .values_list('code', flat=True)
            for story_code in today_stories:
                self.crawler.update_story(story_code)
            time.sleep(FIVE_MINUTES)


class HNSIndexAllStories(HackerNewsService):
    def __init__(self, start_id=1, offset=1):
        super(HNSIndexAllStories, self).__init__()
        self.start_id = start_id
        self.offset = offset

    def run(self):
        self.crawler.index_all_stories(self.start_id, self.offset)


def main():
    HNSUpdateTopStories().start()
    HNSUpdateTodayStoriesData().start()

    HNSIndexAllStories(start_id=29289, offset=2).start()
    HNSIndexAllStories(start_id=29290, offset=2).start()


if __name__ == '__main__':
    main()
