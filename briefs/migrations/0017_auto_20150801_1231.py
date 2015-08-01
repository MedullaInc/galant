# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0016_auto_20150801_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='brief',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]
