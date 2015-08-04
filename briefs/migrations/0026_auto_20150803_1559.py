# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0025_brief_modified'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClientBrief',
        ),
        migrations.DeleteModel(
            name='ProjectBrief',
        ),
        migrations.DeleteModel(
            name='ServiceBrief',
        ),
    ]
