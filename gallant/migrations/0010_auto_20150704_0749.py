# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0009_auto_20150704_0735'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ULText',
        ),
        migrations.AddField(
            model_name='service',
            name='description',
            field=gallant.models.ULCharField(null=True),
        ),
    ]
