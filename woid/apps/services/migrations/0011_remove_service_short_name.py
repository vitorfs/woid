# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_service_short_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='short_name',
        ),
    ]
