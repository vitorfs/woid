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

from woid.crawler.crawler import RedditCrawler
from woid.apps.services.models import Service, Story


FIVE_MINUTES = 5 * 60
REDDIT_SLUG = 'reddit'


class RedditService(threading.Thread):
    def __init__(self):
        super(RedditService, self).__init__()
        self.crawler = RedditCrawler()
        self.service = Service.objects.get(slug=REDDIT_SLUG)


class RSUpdateTopStories(RedditService):
    def run(self):
        while True:
            self.crawler.update_top_stories()
            time.sleep(FIVE_MINUTES)


def main():
    RSUpdateTopStories().start()


if __name__ == '__main__':
    main()
