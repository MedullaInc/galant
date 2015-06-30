# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0004_auto_20150630_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.CharField(max_length=2, choices=[(b'0', b'APPROACHED'), (b'8', b'BLACKLISTED'), (b'2', b'BRIEF_SENT'), (b'7', b'CHECK_NOTES'), (b'6', b'PAST_DUE'), (b'4', b'PENDING_DELIVERABLES'), (b'3', b'PENDING_PAYMENT'), (b'1', b'QUOTED'), (b'5', b'SETTLED')]),
        ),
    ]
