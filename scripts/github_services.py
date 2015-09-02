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

from woid.crawler.crawler import GithubCrawler
from woid.apps.services.models import Service, Story


THIRTY_MINUTES = 30 * 60
GITHUB_SLUG = 'github'


class GithubService(threading.Thread):
    def __init__(self):
        super(GithubService, self).__init__()
        self.crawler = GithubCrawler()
        self.service = Service.objects.get(slug=GITHUB_SLUG)


class GSUpdateTrendingRepositories(GithubService):
    def run(self):
        while True:
            self.crawler.update_today_trending_repositories()
            time.sleep(THIRTY_MINUTES)


def main():
    GSUpdateTrendingRepositories().start()


if __name__ == '__main__':
    main()
