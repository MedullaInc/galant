# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0009_auto_20150908_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quote',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quotetemplate',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quotetemplate',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='section',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='section',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
    ]
