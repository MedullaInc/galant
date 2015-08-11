# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0006_auto_20150810_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='address_2',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
