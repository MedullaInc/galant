# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_auto_20150710_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quote', models.ForeignKey(to='quotes.Quote')),
            ],
        ),
    ]
