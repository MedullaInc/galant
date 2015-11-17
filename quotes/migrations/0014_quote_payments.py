# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0021_payment'),
        ('quotes', '0013_servicesection_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='payments',
            field=models.ManyToManyField(to='gallant.Payment', blank=True),
        ),
    ]
