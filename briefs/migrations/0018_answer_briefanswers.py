# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0017_auto_20150801_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=1000)),
                ('question', models.ForeignKey(to='briefs.Question')),
            ],
        ),
        migrations.CreateModel(
            name='BriefAnswers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answers', models.ManyToManyField(to='briefs.Answer')),
                ('brief', models.ForeignKey(to='briefs.Brief')),
            ],
        ),
    ]
