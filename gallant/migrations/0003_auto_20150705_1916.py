# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0002_service_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='description',
            field=gallant.models.ULTextField(null=True),
        ),
    ]
