# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_auto_20151117_0952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ('name',), 'verbose_name': 'service', 'verbose_name_plural': 'services'},
        ),
    ]
