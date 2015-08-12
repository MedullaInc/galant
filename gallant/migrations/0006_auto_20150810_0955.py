# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0005_auto_20150810_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='country',
            field=django_countries.fields.CountryField(default=b'US', max_length=2),
        ),
    ]
