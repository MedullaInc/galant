# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0006_auto_20150723_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='services',
            field=models.ManyToManyField(related_name='services', to='quotes.ServiceSection', blank=True),
        ),
        migrations.AddField(
            model_name='section',
            name='index',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quote',
            name='sections',
            field=models.ManyToManyField(related_name='sections', to='quotes.Section', blank=True),
        ),
    ]
