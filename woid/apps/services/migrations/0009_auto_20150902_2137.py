# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_story_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='start_comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='story',
            name='start_score',
            field=models.IntegerField(default=0),
        ),
    ]
