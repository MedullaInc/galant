# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0008_auto_20150728_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='BriefTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('brief', models.ForeignKey(to='briefs.Brief')),
            ],
        ),
    ]
