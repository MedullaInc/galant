# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0024_auto_20151130_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(regex=b'^\\+?\\d{0,3} ?(\\(\\d{1,3}\\))?[\\- \\d]+$', message=b"Phone number must be entered in the format: '+99 (999) 999-9999'. Up to 16 digits allowed.")]),
        ),
    ]
