# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20150829_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='content_type',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'T', b'Text'), (b'U', b'URL'), (b'I', b'Image')]),
        ),
        migrations.AlterField(
            model_name='story',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 30, 15, 59, 40, 507961, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
