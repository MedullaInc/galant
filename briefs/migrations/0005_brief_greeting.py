# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.fields


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0004_auto_20150806_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='brief',
            name='greeting',
            field=gallant.fields.ULCharField(help_text=b'Greeting text.', max_length=2000, blank=True),
        ),
    ]
