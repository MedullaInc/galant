# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0020_longanswerquestion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='answer',
        ),
        migrations.CreateModel(
            name='MultipleChoiceAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='briefs.Answer')),
                ('choices', jsonfield.fields.JSONField()),
            ],
            bases=('briefs.answer',),
        ),
        migrations.CreateModel(
            name='TextAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='briefs.Answer')),
                ('answer', models.CharField(max_length=1000)),
            ],
            bases=('briefs.answer',),
        ),
    ]
