# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0005_section_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='intro',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='margin_section',
        ),
    ]
