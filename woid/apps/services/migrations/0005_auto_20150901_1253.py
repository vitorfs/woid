# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_story_top_ten'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='content',
            field=models.TextField(null=True, blank=True),
        ),
    ]
