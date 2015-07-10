# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0002_auto_20150710_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='margin_section',
            field=models.ForeignKey(related_name='margin_section', to='quotes.Section', help_text=b'This section appears on the margin of the last page of a quote.', null=True),
        ),
    ]
