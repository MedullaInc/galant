# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_analysis', '0002_auto_20151119_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerlead',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]
