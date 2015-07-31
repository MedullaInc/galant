# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0009_brieftemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='brief',
            name='name',
            field=models.CharField(default=b'New Brief', max_length=512),
        ),
    ]
