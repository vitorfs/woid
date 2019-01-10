# coding: utf-8

import logging
import re

from django.conf import settings
from django.utils import timezone

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class AbstractBaseClient:
    def __init__(self):
        self.headers = {'user-agent': 'woid/1.0'}


class HackerNewsClient(AbstractBaseClient):
    base_url = 'https://hacker-news.firebaseio.com'

    def request(self, endpoint):
        r = requests.get(endpoint, headers=self.headers)
        result = r.json()
        return result

    def get_top_stories(self):
        endpoint = '%s/v0/topstories.json' % self.base_url
        return self.request(endpoint)

    def get_story(self, code):
        endpoint = '%s/v0/item/%s.json' % (self.base_url, code)
        return self.request(endpoint)

    def get_max_item(self):
        endpoint = '%s/v0/maxitem.json' % self.base_url
        return self.request(endpoint)


class RedditClient(AbstractBaseClient):

    def get_front_page_stories(self):
        stories = list()

        try:
            r = requests.get('https://www.reddit.com/.json', headers=self.headers)
            result = r.json()
            stories = result['data']['children']
        except ValueError:
            logger.exception('An error occurred while executing RedditClient.get_front_page_stories')

        return stories


class GithubClient(AbstractBaseClient):

    def get_today_trending_repositories(self):
        r = requests.get('https://github.com/trending?since=daily', headers=self.headers)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        repos = soup.select('ol.repo-list li')
        data = list()
        for repo in repos:
            repo_data = dict()
            repo_data['name'] = repo.h3.a.get('href')

            description = repo.p.text
            if description:
                description = description.strip()
            else:
                description = ''
            repo_data['description'] = description

            lang = repo.find(attrs={'itemprop': 'programmingLanguage'})
            if lang:
                repo_data['language'] = lang.text.strip()
            else:
                repo_data['language'] = ''

            stars_text = repo.findAll(text=re.compile('stars today'))
            stars_numbers_only = re.findall(r'\d+', stars_text[0])
            repo_data['stars'] = int(stars_numbers_only[0])

            data.append(repo_data)

        return data


class NYTimesClient(AbstractBaseClient):

    base_url = 'http://api.nytimes.com/svc/mostpopular/v2/'

    def get_most_popular_stories(self):
        data = dict()

        mostviewed_endpoint = '{0}mostviewed/all-sections/1.json?api-key={1}'.format(
            self.base_url,
            settings.NYTIMES_API_KEY
        )
        r = requests.get(mostviewed_endpoint, headers=self.headers)
        json_data = r.json()
        data['mostviewed'] = json_data['results']

        mostemailed_endpoint = '{0}mostemailed/all-sections/1.json?api-key={1}'.format(
            self.base_url,
            settings.NYTIMES_API_KEY
        )
        r = requests.get(mostemailed_endpoint, headers=self.headers)
        json_data = r.json()
        data['mostemailed'] = json_data['results']

        mostshared_endpoint = '{0}mostshared/all-sections/1.json?api-key={1}'.format(
            self.base_url,
            settings.NYTIMES_API_KEY
        )
        r = requests.get(mostshared_endpoint, headers=self.headers)
        json_data = r.json()
        data['mostshared'] = json_data['results']

        return data


class ProductHuntClient(AbstractBaseClient):
    def __init__(self):
        super().__init__()
        extra_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % settings.PRODUCT_HUNT_TOKEN,
            'Host': 'api.producthunt.com'
        }
        self.headers.update(extra_headers)

    def get_top_posts(self):
        today = timezone.now().strftime('%Y-%m-%d')
        r = requests.get('https://api.producthunt.com/v1/posts?day=%s' % today, headers=self.headers)
        data = r.json()
        return data['posts']
