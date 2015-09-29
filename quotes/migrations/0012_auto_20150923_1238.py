# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0011_auto_20150923_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='projects',
            field=models.ManyToManyField(to='gallant.Project', blank=True),
        ),
    ]
