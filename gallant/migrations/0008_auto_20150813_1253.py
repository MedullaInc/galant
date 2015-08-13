# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0007_auto_20150810_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='address',
        ),
        migrations.RemoveField(
            model_name='client',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='client',
            name='contact_info',
            field=models.ForeignKey(to='gallant.ContactInfo', null=True),
        ),
    ]
