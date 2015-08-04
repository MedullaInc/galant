# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brief',
            name='status',
            field=models.CharField(default=0, max_length=2, choices=[(b'0', b'Draft'), (b'1', b'Not_Sent'), (b'2', b'Sent'), (b'3', b'Viewed'), (b'4', b'Answered'), (b'5', b'Rejected')]),
        ),
    ]
