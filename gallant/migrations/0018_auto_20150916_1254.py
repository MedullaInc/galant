# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0017_client_deleted_by_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='note',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='service',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='service',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
    ]
