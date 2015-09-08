# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0014_auto_20150908_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.CharField(max_length=2, choices=[(b'0', b'Approached'), (b'1', b'Quoted'), (b'2', b'Brief_Sent'), (b'3', b'Pending_Payment'), (b'4', b'Pending_Deliverables'), (b'5', b'Settled'), (b'6', b'Past_Due'), (b'7', b'Check_Notes'), (b'8', b'Blacklisted')]),
        ),
    ]
