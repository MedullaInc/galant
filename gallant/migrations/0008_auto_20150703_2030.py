# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0007_auto_20150702_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='name',
            field=gallant.models.ULTextField(),
        ),
    ]
