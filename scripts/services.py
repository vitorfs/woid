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


class HackerNewsService(threading.Thread):

    def __init__(self):
        super(HackerNewsService, self).__init__()
        self.crawler = HackerNewsCrawler()

    def run(self):
        while True:
            print 'Crawling Hacker News top stories...'
            self.crawler.update_top_stories()
            time.sleep(5*60)


def main():
    hn = HackerNewsService()
    hn.start()

if __name__ == '__main__':
    main()
