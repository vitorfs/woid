import time

from django.core.management.base import BaseCommand

from woid.apps.services import crawlers


class Command(BaseCommand):
    help = 'Crawl external services to update top stories'

    def get_crawler_class(self, slug):
        crawlers_classes = {
            'reddit': crawlers.RedditCrawler,
            'medium': crawlers.MediumCrawler,
            'hn': crawlers.HackerNewsCrawler,
            'producthunt': crawlers.ProductHuntCrawler,
            'github': crawlers.GithubCrawler,
            'nytimes': crawlers.NyTimesCrawler,
        }
        return crawlers_classes.get(slug)


    def add_arguments(self, parser):
        parser.add_argument('service_slug', nargs='+', type=str, help='Service Slug')

    def handle(self, *args, **kwargs):
        service_slugs = kwargs['service_slug']
        for slug in service_slugs:
            crawler_class = self.get_crawler_class(slug)
            if crawler_class is not None:
                crawler = crawler_class()
                start_time = time.time()
                crawler.run()
                elapsed_seconds = round(time.time() - start_time, 2)
                self.stdout.write(self.style.SUCCESS('%s crawler executed in %s seconds') % (slug, elapsed_seconds))
            else:
                self.stdout.write(self.style.WARNING('Crawler with slug "%s" not found.') % slug)
