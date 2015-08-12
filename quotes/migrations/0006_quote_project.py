# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0004_auto_20150807_1721'),
        ('quotes', '0005_auto_20150806_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='project',
            field=models.OneToOneField(null=True, to='gallant.Project'),
        ),
    ]
