# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0005_brief_greeting'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='answer',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='brief',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='brief',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='briefanswers',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='briefanswers',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='brieftemplate',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='brieftemplate',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='image',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='image',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
    ]
