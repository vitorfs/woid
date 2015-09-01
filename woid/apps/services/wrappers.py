# coding: utf-8

import logging
import requests
from firebase import firebase

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
