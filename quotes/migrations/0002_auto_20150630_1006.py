# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0004_auto_20150630_1006'),
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='client',
            field=models.ForeignKey(to='gallant.Client', null=True),
        ),
        migrations.AddField(
            model_name='quote',
            name='name',
            field=models.CharField(default=b'New Quote', max_length=512),
        ),
    ]
