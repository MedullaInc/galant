# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0023_auto_20150802_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='briefanswers',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 2, 20, 1, 20, 395377, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
