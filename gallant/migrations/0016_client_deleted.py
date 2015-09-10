# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0015_auto_20150908_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
