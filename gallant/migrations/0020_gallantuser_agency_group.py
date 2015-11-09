# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('gallant', '0019_auto_20151016_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallantuser',
            name='agency_group',
            field=models.ForeignKey(to='auth.Group', null=True),
        ),
    ]
