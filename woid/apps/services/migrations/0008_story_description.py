# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_story_nsfw'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='description',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
