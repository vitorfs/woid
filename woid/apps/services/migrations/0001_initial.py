# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('comments', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('service', models.ForeignKey(to='services.Service')),
            ],
            options={
                'verbose_name': 'story',
                'verbose_name_plural': 'stories',
            },
        ),
        migrations.AlterUniqueTogether(
            name='story',
            unique_together=set([('service', 'code')]),
        ),
    ]
