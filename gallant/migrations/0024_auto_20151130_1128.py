# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0023_client_last_contacted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='note',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='submitted_on',
        ),
        migrations.AddField(
            model_name='payment',
            name='due',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='notes',
            field=models.ManyToManyField(to='gallant.Note'),
        ),
        migrations.AddField(
            model_name='payment',
            name='paid_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
