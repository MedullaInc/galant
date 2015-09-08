# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0008_auto_20150903_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
    ]
