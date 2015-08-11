# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0003_auto_20150805_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='notes',
            field=models.ManyToManyField(to='gallant.Note'),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(default=1, max_length=2, choices=[(b'0', b'On_Hold'), (b'1', b'Pending_Assignment'), (b'2', b'Active'), (b'3', b'Overdue'), (b'4', b'Completed')]),
        ),
    ]
