# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0008_auto_20150703_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='description',
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=gallant.models.ULCharField(),
        ),
    ]
