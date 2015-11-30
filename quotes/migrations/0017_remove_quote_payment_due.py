# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0016_auto_20151123_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='payment_due',
        ),
    ]
