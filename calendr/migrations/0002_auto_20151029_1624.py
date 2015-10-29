# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='start',
            field=models.DateTimeField(),
        ),
    ]
