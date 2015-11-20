# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0014_quote_payments'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='payment_due',
            field=models.DateField(null=True, blank=True),
        ),
    ]
