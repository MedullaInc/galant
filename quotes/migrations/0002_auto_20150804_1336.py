# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textsection',
            name='text',
            field=gallant.fields.ULTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='textsection',
            name='title',
            field=gallant.fields.ULCharField(blank=True),
        ),
    ]
