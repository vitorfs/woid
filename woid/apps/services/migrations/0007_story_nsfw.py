# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20150902_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='nsfw',
            field=models.BooleanField(default=False),
        ),
    ]
