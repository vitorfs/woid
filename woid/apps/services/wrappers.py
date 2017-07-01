# coding: utf-8

import logging
import json
import re

from bs4 import BeautifulSoup
import requests
from firebase import firebase

from django.conf import settings


requests.packages.urllib3.disable_warnings()


class AbstractBaseClient(object):
    def __init__(self):
        self.headers = { 'user-agent': 'woid/1.0' }


class HackerNewsClient(object):
    def __init__(self):
        self.firebase_app = firebase.FirebaseApplication('https://hacker-news.firebaseio.com', None)

    def get_top_stories(self):
        result = self.firebase_app.get('/v0/topstories', None)
        return result

    def get_story(self, code):
        result = self.firebase_app.get('/v0/item/{0}'.format(code), None)
        return result

    def get_max_item(self):
        result = self.firebase_app.get('/v0/maxitem', None)
        return result


class RedditClient(AbstractBaseClient):

    def get_front_page_stories(self):
        r = None
        stories = list()

        try:
            r = requests.get('https://www.reddit.com/.json', headers=self.headers)
            result = r.json()
            stories = result['data']['children']
            count = 25
            while result['data']['after']:
                r = requests.get(u'https://www.reddit.com/.json?count={0}&after={1}'.format(count, result['data']['after']), headers=self.headers)
                result = r.json()
                stories.extend(result['data']['children'])
                count += 25
        except ValueError, e:
            logging.error(e)
            logging.error(r)

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


class MediumClient(AbstractBaseClient):

    def get_top_stories(self):
        r = requests.get('https://medium.com/top-stories?format=json', headers=self.headers)
        text_data = r.text[16:] # remove ])}while(1);</x>
        json_data = json.loads(text_data)
        return json_data['payload']['value']['posts']


class NyTimesClient(AbstractBaseClient):

    def get_most_popular_stories(self):
        data = dict()

        mostviewed_endpoint = 'http://api.nytimes.com/svc/mostpopular/v2/mostviewed/all-sections/1.json?api-key={0}'.format(settings.NYTIMES_API_KEY)
        r = requests.get(mostviewed_endpoint, headers=self.headers)
        json_data = r.json()
        data['mostviewed'] = json_data['results']

        mostemailed_endpoint = 'http://api.nytimes.com/svc/mostpopular/v2/mostemailed/all-sections/1.json?api-key={0}'.format(settings.NYTIMES_API_KEY)
        r = requests.get(mostemailed_endpoint, headers=self.headers)
        json_data = r.json()
        data['mostemailed'] = json_data['results']

        mostshared_endpoint = 'http://api.nytimes.com/svc/mostpopular/v2/mostshared/all-sections/1.json?api-key={0}'.format(settings.NYTIMES_API_KEY)
        r = requests.get(mostshared_endpoint, headers=self.headers)
        json_data = r.json()
        data['mostshared'] = json_data['results']

        return data

class DiggClient(AbstractBaseClient):

    def get_top_stories(self):
        r = requests.get('http://digg.com/', headers=self.headers)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        diggs = soup(attrs={ 'class': 'digg-story' })

        data = list()
        for digg in diggs:
            story_data = dict()
            title = digg.find(attrs={ 'class': 'entry-title' })
            story_data['title'] = title.text.strip()
            try:
                story_data['score'] = int(re.sub(r'\D', '', digg['data-digg-score']))
            except:
                story_data['score'] = 0
            story_data['id'] = digg['data-content-id']
            story_data['url'] = digg['data-contenturl']
            data.append(story_data)

        return data
