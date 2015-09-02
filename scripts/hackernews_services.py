from unipath import Path
import sys
import os

PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woid.settings')

import django
django.setup()


import logging
import time
import threading

from django.utils import timezone

from woid.crawler.crawler import HackerNewsCrawler
from woid.apps.services.models import Service, Story


FIVE_MINUTES = 5 * 60
TWELVE_HOURS = 12 * 60 * 60
HACKER_NEWS_SLUG = 'hn'


class HackerNewsService(threading.Thread):
    def __init__(self):
        super(HackerNewsService, self).__init__()
        self.crawler = HackerNewsCrawler()
        self.service = Service.objects.get(slug=HACKER_NEWS_SLUG)


class HNSUpdateTopStories(HackerNewsService):
    def run(self):
        logging.debug('HNSUpdateTopStories: Starting')
        run_count = 0
        while True:
            run_count = run_count + 1
            logging.debug('HNSUpdateTopStories: Run #{0}'.format(run_count))
            logging.debug('HNSUpdateTopStories: Updating top stories')
            self.crawler.update_top_stories()
            logging.debug('HNSUpdateTopStories: Sleeping for 5 minutes')
            time.sleep(FIVE_MINUTES)


class HNSUpdateTodayStoriesData(HackerNewsService):
    def run(self):
        logging.debug('HNSUpdateTodayStoriesData: Starting')
        run_count = 0
        while True:
            run_count = run_count + 1
            logging.debug('HNSUpdateTodayStoriesData: Run #{0}'.format(run_count))
            today = timezone.now()
            logging.debug('HNSUpdateTodayStoriesData: Reference day {0}'.format(today))
            today_stories = self.service.stories \
                    .filter(date__year=today.year, date__month=today.month, date__day=today.day) \
                    .values_list('code', flat=True)
            for story_code in today_stories:
                logging.debug('HNSUpdateTodayStoriesData: Crawling HN story with id {0}'.format(story_code))
                self.crawler.update_story(story_code)
            logging.debug('HNSUpdateTodayStoriesData: Sleeping for 5 minutes')
            time.sleep(FIVE_MINUTES)


class HNSUpdateOldStoriesData(HackerNewsService):
    def run(self):
        logging.debug('HNSUpdateOldStoriesData: Starting')
        run_count = 0
        while True:
            run_count = run_count + 1
            logging.debug('HNSUpdateOldStoriesData: Run #{0}'.format(run_count))
            stories = self.service.stories.all().values_list('code', flat=True)
            for story_code in stories:
                self.crawler.update_story(story_code)
            logging.debug('HNSUpdateOldStoriesData: Sleeping for 12 hours')
            time.sleep(TWELVE_HOURS)

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
    HNSUpdateOldStoriesData().start()
    HNSIndexAllStories().start()
    '''
    HNSIndexAllStories(start_id=1, offset=3).start()
    HNSIndexAllStories(start_id=2, offset=3).start()
    HNSIndexAllStories(start_id=3, offset=3).start()
    '''
if __name__ == '__main__':
    main()
