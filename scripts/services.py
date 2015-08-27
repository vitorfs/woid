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

from woid.crawler.crawler import HackerNewsCrawler
from woid.apps.services.models import Service, Story


class HNSUpdateTopStories(threading.Thread):
    crawler = HackerNewsCrawler()

    def run(self):
        while True:
            print 'Searching for new Hacker News top stories...'
            self.crawler.update_top_stories()
            time.sleep(5*60)

class HNSUpdateStoriesData(threading.Thread):
    crawler = HackerNewsCrawler()
    service = Service.objects.get(slug='hn')
    def run(self):
        while True:
            print 'Updating Hacker News top stories...'
            for story in Story.objects.all():
                self.crawler.update_story(story)

def main():
    HNSUpdateTopStories().start()
    HNSUpdateStoriesData().start()
    

if __name__ == '__main__':
    main()
