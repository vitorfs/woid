# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('base_url', models.URLField()),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=500, null=True, blank=True)),
                ('url', models.URLField(max_length=2000, null=True, blank=True)),
                ('content', models.CharField(max_length=4000, null=True, blank=True)),
                ('content_type', models.CharField(default=b'T', max_length=1, choices=[(b'T', b'Text'), (b'U', b'URL')])),
                ('comments', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(default=b'N', max_length=1, choices=[(b'N', b'New'), (b'O', b'Ok'), (b'E', b'Error')])),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to='services.Service')),
            ],
            options={
                'ordering': ('-score',),
                'verbose_name': 'story',
                'verbose_name_plural': 'stories',
            },
        ),
        migrations.CreateModel(
            name='StoryUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comments_changes', models.IntegerField(default=0)),
                ('score_changes', models.IntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='services.Story')),
            ],
            options={
                'db_table': 'services_story_update',
                'verbose_name': 'story update',
                'verbose_name_plural': 'stories updates',
            },
        ),
        migrations.AlterUniqueTogether(
            name='story',
            unique_together=set([('service', 'code', 'date')]),
        ),
    ]
