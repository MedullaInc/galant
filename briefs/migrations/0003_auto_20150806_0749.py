# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0002_auto_20150804_1349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'permissions': (('view_answer', 'View answer'),)},
        ),
        migrations.AlterModelOptions(
            name='brief',
            options={'permissions': (('view_brief', 'View brief'),)},
        ),
        migrations.AlterModelOptions(
            name='briefanswers',
            options={'permissions': (('view_briefanswers', 'View briefanswers'),)},
        ),
        migrations.AlterModelOptions(
            name='brieftemplate',
            options={'permissions': (('view_brieftemplate', 'View brieftemplate'),)},
        ),
        migrations.AlterModelOptions(
            name='imagequestion',
            options={'permissions': (('view_imagequestion', 'View imagequestion'),)},
        ),
        migrations.AlterModelOptions(
            name='multiplechoiceanswer',
            options={'permissions': (('view_multiplechoiceanswer', 'View multiplechoiceanswer'),)},
        ),
        migrations.AlterModelOptions(
            name='multiplechoicequestion',
            options={'permissions': (('view_multiplechoicequestion', 'View multiplechoicequestion'),)},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'permissions': (('view_question', 'View question'),)},
        ),
        migrations.AlterModelOptions(
            name='textanswer',
            options={'permissions': (('view_textanswer', 'View textanswer'),)},
        ),
        migrations.AlterModelOptions(
            name='textquestion',
            options={'permissions': (('view_textquestion', 'View textquestion'),)},
        ),
        migrations.AddField(
            model_name='textquestion',
            name='is_long_answer',
            field=models.BooleanField(default=False),
        ),
    ]
