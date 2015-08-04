# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0018_answer_briefanswers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OpenQuestion',
        ),
        migrations.DeleteModel(
            name='QuestionTemplate',
        ),
    ]
