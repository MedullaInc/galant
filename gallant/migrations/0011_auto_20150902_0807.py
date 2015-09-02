# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0010_auto_20150902_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='phone_number',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,16}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 16 digits allowed.")]),
        ),
    ]
