# coding: utf-8

from unipath import Path
import sys
import os

PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woid.settings')

import django
from django.utils import timezone
django.setup()


from twisted.internet import task
from twisted.internet import reactor

from woid.apps.services.models import Service
from woid.apps.services import crawlers


FIVE_MINUTES = 5 * 60
THIRTY_MINUTES = 30 * 60

def crawler_run(crawler):
    try:
        crawler.service.status = Service.CRAWLING
        crawler.service.last_run = timezone.now()
        crawler.service.save()
        crawler.update_top_stories()
        crawler.service.status = Service.GOOD
        crawler.service.save()
    except Exception, e:
        crawler.service.status = Service.ERROR
        crawler.service.save()

def hn_loop_task():
    crawler = crawlers.HackerNewsCrawler()
    crawler_run(crawler)

def reddit_loop_task():
    crawler = crawlers.RedditCrawler()
    crawler_run(crawler)

def medium_loop_task():
    crawler = crawlers.MediumCrawler()
    crawler_run(crawler)

def digg_loop_task():
    crawler = crawlers.DiggCrawler()
    crawler_run(crawler)

def github_loop_task():
    crawler = crawlers.GithubCrawler()
    crawler_run(crawler)

def nytimes_loop_task():
    crawler = crawlers.NyTimesCrawler()
    crawler_run(crawler)


def main():
    task.LoopingCall(hn_loop_task).start(FIVE_MINUTES)
    task.LoopingCall(reddit_loop_task).start(FIVE_MINUTES)
    task.LoopingCall(medium_loop_task).start(FIVE_MINUTES)
    task.LoopingCall(digg_loop_task).start(FIVE_MINUTES)

    task.LoopingCall(github_loop_task).start(THIRTY_MINUTES)
    task.LoopingCall(nytimes_loop_task).start(THIRTY_MINUTES)

    reactor.run()

if __name__ == '__main__':
    main()
