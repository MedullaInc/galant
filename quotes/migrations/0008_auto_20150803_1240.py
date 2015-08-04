# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0007_auto_20150723_2034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='created',
        ),
        migrations.AddField(
            model_name='quote',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 3, 19, 40, 8, 878514, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
