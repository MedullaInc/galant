# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0013_auto_20150908_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='address',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='city',
            field=models.CharField(max_length=127, blank=True),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(regex=b'^\\+?\\d{0,3}\\(?\\d{1,3}\\)\\d+\\-\\d{1,10}$|^\\+?\\d{0,3}\\-?\\d{1,3}\\-\\d+\\-\\d{1,10}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 16 digits allowed.")]),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='state',
            field=models.CharField(max_length=127, blank=True),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='zip',
            field=models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(regex=b'^\\d{5}(?:[-\\s]\\d{4})?$', message=b"Zipcode must be entered in the format: '12345-1234' (first five digits required).")]),
        ),
    ]
