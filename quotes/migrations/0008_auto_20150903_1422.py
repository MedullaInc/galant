# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


def fill_quote_tokens(apps, schema_editor):
    Quote = apps.get_model('quotes', 'Quote')
    quotes = Quote.objects.filter(token=None)

    for quote in quotes: # pragma: no cover
        quote.token = uuid.uuid4()
        quote.save()


class Migration(migrations.Migration):
    dependencies = [
        ('quotes', '0007_auto_20150814_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='token',
            field=models.UUIDField(unique=False, null=True),
        ),
        migrations.RunPython(fill_quote_tokens),
        migrations.AlterField(
            model_name='quote',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
