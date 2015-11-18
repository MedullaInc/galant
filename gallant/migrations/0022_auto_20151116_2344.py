# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0021_payment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'permissions': (('view_payment', 'View payment'),)},
        ),
    ]
