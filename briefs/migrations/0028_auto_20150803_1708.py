# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0027_auto_20150803_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brief',
            name='client',
            field=models.ForeignKey(to='gallant.Client', null=True),
        ),
    ]
