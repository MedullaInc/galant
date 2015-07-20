# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_quotetemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='name',
            field=models.CharField(default=b'section', max_length=256),
        ),
    ]
