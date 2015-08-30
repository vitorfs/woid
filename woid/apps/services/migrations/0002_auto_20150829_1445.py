# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='base_url',
        ),
        migrations.AddField(
            model_name='service',
            name='story_url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
