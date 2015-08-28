# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20150828_0953'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=500, null=True, blank=True)),
                ('comments', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('story', models.ForeignKey(related_name='updates', to='services.Story')),
            ],
        ),
    ]
