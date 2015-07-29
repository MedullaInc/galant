# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0006_auto_20150716_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='brief',
            name='questions',
            field=models.ManyToManyField(to='briefs.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='index',
            field=models.IntegerField(default=0),
        ),
    ]
