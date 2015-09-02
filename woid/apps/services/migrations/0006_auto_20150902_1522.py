# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20150901_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='content_type',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'T', b'text'), (b'U', b'url'), (b'I', b'image')]),
        ),
        migrations.AlterField(
            model_name='story',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
