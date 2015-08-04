# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('briefs', '0022_auto_20150802_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_briefs.answer_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_briefs.question_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
    ]
