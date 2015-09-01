# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20150830_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='top_ten',
            field=models.BooleanField(default=False),
        ),
    ]
