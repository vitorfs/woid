# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_auto_20150902_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='short_name',
            field=models.CharField(default='1', max_length=20),
            preserve_default=False,
        ),
    ]
