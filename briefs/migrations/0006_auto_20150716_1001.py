# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.fields


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0005_auto_20150716_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brief',
            name='title',
            field=gallant.fields.ULCharField(help_text=b'Brief title.', max_length=255),
        ),
    ]
