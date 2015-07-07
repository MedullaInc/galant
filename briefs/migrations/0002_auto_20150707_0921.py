# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.models


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='choices',
            field=gallant.models.ULTextArrayField(),
        ),
    ]
