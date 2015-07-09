# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0002_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Brief',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(help_text=b'Brief title.')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=255)),
                ('help_text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BriefTemplate',
            fields=[
                ('brief_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='briefs.Brief')),
            ],
            bases=('briefs.brief',),
        ),
        migrations.CreateModel(
            name='ClientBrief',
            fields=[
                ('brief_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='briefs.Brief')),
                ('client', models.ForeignKey(to='gallant.Client')),
            ],
            bases=('briefs.brief',),
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='briefs.Question')),
                ('can_select_multiple', models.BooleanField(default=False)),
                ('choices', gallant.fields.ULTextField()),
            ],
            bases=('briefs.question',),
        ),
        migrations.CreateModel(
            name='OpenQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='briefs.Question')),
                ('is_long_answer', models.BooleanField(default=False)),
            ],
            bases=('briefs.question',),
        ),
        migrations.CreateModel(
            name='ProjectBrief',
            fields=[
                ('brief_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='briefs.Brief')),
                ('project', models.ForeignKey(to='gallant.Project')),
            ],
            bases=('briefs.brief',),
        ),
        migrations.CreateModel(
            name='QuestionTemplate',
            fields=[
                ('question_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='briefs.Question')),
            ],
            bases=('briefs.question',),
        ),
        migrations.CreateModel(
            name='ServiceBrief',
            fields=[
                ('brief_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='briefs.Brief')),
                ('service', models.ForeignKey(to='gallant.Service')),
            ],
            bases=('briefs.brief',),
        ),
        migrations.AddField(
            model_name='answer',
            name='brief',
            field=models.ForeignKey(to='briefs.Brief'),
        ),
        migrations.CreateModel(
            name='ImageQuestion',
            fields=[
                ('multiplechoicequestion_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='briefs.MultipleChoiceQuestion')),
            ],
            bases=('briefs.multiplechoicequestion',),
        ),
    ]
