# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0016_client_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='deleted_by_parent',
            field=models.BooleanField(default=False),
        ),
    ]
