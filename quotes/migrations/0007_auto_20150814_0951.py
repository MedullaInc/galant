# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0006_quote_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesection',
            name='service',
            field=gallant.models.UnsavedForeignKey(to='gallant.Service'),
        ),
    ]
