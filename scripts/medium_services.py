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

from woid.crawler.crawler import MediumCrawler
from woid.apps.services.models import Service, Story


FIVE_MINUTES = 5 * 60
MEDIUM_SLUG = 'medium'


class MediumService(threading.Thread):
    def __init__(self):
        super(MediumService, self).__init__()
        self.crawler = MediumCrawler()
        self.service = Service.objects.get(slug=MEDIUM_SLUG)


class MSUpdateTopStories(MediumService):
    def run(self):
        while True:
            self.crawler.update_top_stories()
            time.sleep(FIVE_MINUTES)


def main():
    MSUpdateTopStories().start()


if __name__ == '__main__':
    main()
