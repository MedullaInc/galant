# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0019_auto_20150801_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='LongAnswerQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='briefs.Question')),
            ],
            bases=('briefs.question',),
        ),
    ]
