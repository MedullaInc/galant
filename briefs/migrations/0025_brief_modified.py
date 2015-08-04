# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0024_briefanswers_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='brief',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 3, 19, 39, 59, 581460, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
