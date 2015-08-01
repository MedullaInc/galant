# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0011_auto_20150731_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brief',
            name='token',
            field=models.CharField(default=uuid.uuid4, max_length=64, unique=True, null=True, help_text=b'For emailing URL'),
        ),
    ]
