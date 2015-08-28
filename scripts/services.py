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


class HNSUpdateTopStories(threading.Thread):
    crawler = HackerNewsCrawler()
    def run(self):
        print('HNSUpdateTopStories: Starting')
        run_count = 0
        while True:
            run_count = run_count + 1
            print('HNSUpdateTopStories: Run #{0}'.format(run_count))
            print('HNSUpdateTopStories: Updating top stories')
            self.crawler.update_top_stories()
            print('HNSUpdateTopStories: Sleeping for 5 minutes')
            time.sleep(FIVE_MINUTES)


class HNSUpdateTodayStoriesData(threading.Thread):
    crawler = HackerNewsCrawler()
    service = Service.objects.get(slug='hn')
    def run(self):
        print('HNSUpdateTodayStoriesData: Starting')
        run_count = 0
        while True:
            run_count = run_count + 1
            print('HNSUpdateTodayStoriesData: Run #{0}'.format(run_count))
            today = timezone.now()
            print('HNSUpdateTodayStoriesData: Reference day {0}'.format(today))
            today_stories = self.service.stories.filter(date__year=today.year, date__month=today.month, date__day=today.day)
            for story in today_stories:
                print('HNSUpdateTodayStoriesData: Crawling HN story with id {0}'.format(story.pk))
                self.crawler.update_story(story)
            print('HNSUpdateTodayStoriesData: Sleeping for 5 minutes')
            time.sleep(FIVE_MINUTES)


class HNSUpdateOldStoriesData(threading.Thread):
    crawler = HackerNewsCrawler()
    service = Service.objects.get(slug='hn')
    def run(self):
        print('HNSUpdateOldStoriesData: Starting')
        run_count = 0
        while True:
            run_count = run_count + 1
            print('HNSUpdateOldStoriesData: Run #{0}'.format(run_count))
            for story in self.service.stories.all():
                self.crawler.update_story(story)
            print('HNSUpdateOldStoriesData: Sleeping for 12 hours')
            time.sleep(TWELVE_HOURS)


def main():
    HNSUpdateTopStories().start()
    HNSUpdateTodayStoriesData().start()
    HNSUpdateOldStoriesData().start()


if __name__ == '__main__':
    main()
