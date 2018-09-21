from django.contrib.auth.models import User
from django.db import models


class Feed(models.Model):
    url = models.URLField(unique=True)
    last_update = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=300)
    url = models.URLField()
    date = models.DateTimeField()


class Subscription(models.Model):
    user = models.ForeignKey(User)
    feed = models.ForeignKey(Feed)
