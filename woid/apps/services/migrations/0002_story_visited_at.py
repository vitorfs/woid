# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='visited_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 27, 9, 5, 30, 940716, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
