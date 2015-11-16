# coding: utf-8

import logging
import json
import re

from bs4 import BeautifulSoup
import requests
from firebase import firebase

from django.conf import settings


requests.packages.urllib3.disable_warnings()


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


class RedditClient(object):
    def __init__(self):
        self.headers = { 'user-agent': 'woid/1.0' }

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


class GithubClient(object):
    def __init__(self):
        self.headers = { 'user-agent': 'woid/1.0' }

    def get_today_trending_repositories(self):
        r = requests.get('https://github.com/trending', headers=self.headers)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        repos = soup(attrs={ 'class': 'repo-list-item' })
        data = list()
        for repo in repos:
            repo_data = dict()
            repo_data['name'] = repo.h3.a.get('href')

            description = repo.find(attrs={'class': 'repo-list-description'})
            if description:
                description = description.text.strip()
            else:
                description = ''
            repo_data['description'] = description

            repo_meta = repo.find(attrs={'class': 'repo-list-meta'})
            if repo_meta:
                repo_meta = repo_meta.text.split()
                if len(repo_meta) == 8: # means we have the repo language
                    repo_data['language'] = repo_meta[0]
                    repo_data['stars'] = int(re.sub(r'\D', '', repo_meta[2]))
                elif len(repo_meta) == 6: # means we do not have repo language
                    repo_data['language'] = ''
                    repo_data['stars'] = int(re.sub(r'\D', '', repo_meta[0]))

            data.append(repo_data)
        
        return data


class MediumClient(object):
    def __init__(self):
        self.headers = { 'user-agent': 'woid/1.0' }

    def get_top_stories(self):
        r = requests.get('https://medium.com/top-stories?format=json', headers=self.headers)
        text_data = r.text[16:] # remove ])}while(1);</x>
        json_data = json.loads(text_data)
        return json_data['payload']['value']['posts']


class NyTimesClient(object):
    def __init__(self):
        self.headers = { 'user-agent': 'woid/1.0' }

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
