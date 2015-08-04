# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0021_auto_20150801_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textanswer',
            name='answer',
            field=models.CharField(max_length=3000),
        ),
    ]
