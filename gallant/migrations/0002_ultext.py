# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ULText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_dict', jsonfield.fields.JSONField(help_text=b'JSON formatted dictionary mapping                           [IETF language code -> translation in that language]', max_length=60000)),
            ],
        ),
    ]
