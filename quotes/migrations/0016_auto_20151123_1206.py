# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0015_quote_payment_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='services',
            field=models.ManyToManyField(to='quotes.ServiceSection', blank=True),
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='services',
            new_name='service_sections',
        ),
        migrations.AlterField(
            model_name='quote',
            name='sections',
            field=models.ManyToManyField(to='quotes.TextSection', blank=True),
        ),
    ]
