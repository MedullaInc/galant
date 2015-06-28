# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0003_service'),
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceSection',
            fields=[
                ('section_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='quotes.Section')),
                ('service', models.ForeignKey(to='gallant.Service')),
            ],
            bases=('quotes.section',),
        ),
    ]
