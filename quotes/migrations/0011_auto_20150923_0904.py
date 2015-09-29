# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0018_auto_20150916_1254'),
        ('quotes', '0010_auto_20150916_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='project',
        ),
        migrations.AddField(
            model_name='quote',
            name='projects',
            field=models.ManyToManyField(to='gallant.Project'),
        ),
    ]
