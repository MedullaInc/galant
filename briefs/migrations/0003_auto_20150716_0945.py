# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0002_auto_20150707_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='brief',
            name='status',
            field=models.CharField(default=0, max_length=2, choices=[(b'4', b'Answered'), (b'0', b'Draft'), (b'1', b'Not_Sent'), (b'5', b'Rejected'), (b'2', b'Sent'), (b'3', b'Viewed')]),
        ),
        migrations.AddField(
            model_name='brief',
            name='token',
            field=models.CharField(help_text=b'For emailing URL', max_length=64, unique=True, null=True),
        ),
    ]
