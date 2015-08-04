# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='size',
            field=models.CharField(max_length=2, choices=[(b'0', b'Micro'), (b'1', b'Small'), (b'2', b'Medium'), (b'3', b'Large')]),
        ),
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.CharField(max_length=2, choices=[(b'0', b'Approached'), (b'1', b'Quoted'), (b'2', b'Brief_Sent'), (b'3', b'Pending_Payment'), (b'4', b'Pending_Deliverables'), (b'5', b'Settled'), (b'6', b'Past_Due'), (b'7', b'Check_Notes'), (b'8', b'Blacklisted')]),
        ),
        migrations.AlterField(
            model_name='service',
            name='type',
            field=models.CharField(max_length=2, choices=[(b'0', b'Branding'), (b'1', b'Design'), (b'2', b'Architecture'), (b'3', b'Advertising'), (b'4', b'Production'), (b'5', b'Illustration'), (b'6', b'Industrial_Design'), (b'7', b'Fashion_Design'), (b'8', b'Interior_Design')]),
        ),
    ]
