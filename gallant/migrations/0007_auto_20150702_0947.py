# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0006_auto_20150630_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='size',
            field=models.CharField(max_length=2, choices=[(b'3', b'Large'), (b'2', b'Medium'), (b'0', b'Micro'), (b'1', b'Small')]),
        ),
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.CharField(max_length=2, choices=[(b'0', b'Approached'), (b'8', b'Blacklisted'), (b'2', b'Brief_Sent'), (b'7', b'Check_Notes'), (b'6', b'Past_Due'), (b'4', b'Pending_Deliverables'), (b'3', b'Pending_Payment'), (b'1', b'Quoted'), (b'5', b'Settled')]),
        ),
        migrations.AlterField(
            model_name='client',
            name='type',
            field=models.CharField(max_length=2, choices=[(b'0', b'Individual'), (b'1', b'Organization')]),
        ),
        migrations.AlterField(
            model_name='service',
            name='type',
            field=models.CharField(max_length=2, choices=[(b'3', b'Advertising'), (b'2', b'Architecture'), (b'0', b'Branding'), (b'1', b'Design'), (b'7', b'Fashion_Design'), (b'5', b'Illustration'), (b'6', b'Industrial_Design'), (b'8', b'Interior_Design'), (b'4', b'Production')]),
        ),
    ]
