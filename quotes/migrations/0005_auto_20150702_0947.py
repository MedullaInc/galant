# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_auto_20150630_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='status',
            field=models.CharField(default=0, max_length=2, choices=[(b'5', b'Accepted'), (b'0', b'Draft'), (b'1', b'Not_Sent'), (b'6', b'Rejected'), (b'2', b'Sent'), (b'4', b'Superseded'), (b'3', b'Viewed')]),
        ),
    ]
