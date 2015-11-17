# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_remove_service_short_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='last_run',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='service',
            name='status',
            field=models.CharField(default=b'G', max_length=1, choices=[(b'G', '\u2713 good'), (b'E', '\xd7 error'), (b'C', '~ running')]),
        ),
    ]
