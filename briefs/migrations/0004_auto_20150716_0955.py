# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0003_auto_20150716_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brief',
            name='title',
            field=models.CharField(help_text=b'Brief title.', max_length=255),
        ),
    ]
