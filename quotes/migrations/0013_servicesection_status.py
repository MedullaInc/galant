# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0012_auto_20150923_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesection',
            name='status',
            field=models.CharField(default=1, max_length=2, choices=[(b'0', b'On_Hold'), (b'1', b'Pending_Assignment'), (b'2', b'Active'), (b'3', b'Overdue'), (b'4', b'Completed')]),
        ),
    ]
