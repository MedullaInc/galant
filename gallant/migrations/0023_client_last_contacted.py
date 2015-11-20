# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0022_auto_20151116_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='last_contacted',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
