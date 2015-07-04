# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0005_auto_20150702_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='text',
            field=gallant.models.ULTextField(),
        ),
        migrations.AlterField(
            model_name='section',
            name='title',
            field=gallant.models.ULCharField(),
        ),
    ]
