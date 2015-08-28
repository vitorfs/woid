# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_story_visited_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ('-score',), 'verbose_name': 'story', 'verbose_name_plural': 'stories'},
        ),
        migrations.AlterField(
            model_name='story',
            name='service',
            field=models.ForeignKey(related_name='stories', to='services.Service'),
        ),
        migrations.AlterField(
            model_name='story',
            name='title',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='url',
            field=models.URLField(max_length=2000, null=True, blank=True),
        ),
    ]
