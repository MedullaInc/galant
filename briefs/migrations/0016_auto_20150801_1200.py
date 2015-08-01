# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0015_auto_20150801_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brief',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
