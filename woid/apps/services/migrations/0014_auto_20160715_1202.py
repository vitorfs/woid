# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0013_auto_20151117_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='date',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
    ]
