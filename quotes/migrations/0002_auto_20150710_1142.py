# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='notes',
        ),
        migrations.AddField(
            model_name='quote',
            name='margin_section',
            field=models.ForeignKey(related_name='notes', to='quotes.Section', help_text=b'This section appears on the margin of the last page of a quote.', null=True),
        ),
    ]
