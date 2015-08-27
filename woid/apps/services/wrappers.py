# coding: utf-8

from firebase import firebase


class HackerNews(object):
    def __init__(self):
        self.firebase_app = firebase.FirebaseApplication('https://hacker-news.firebaseio.com', None)

    def get_top_stories(self):
        results = self.firebase_app.get('/v0/topstories', None)
        return results

    def get_story(self, code):
        result = self.firebase_app.get('/v0/item/{0}'.format(code), None)
        return result
