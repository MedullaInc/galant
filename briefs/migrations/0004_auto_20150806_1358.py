# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0003_auto_20150806_0749'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagequestion',
            options={'permissions': (('view_imagequestion', 'View imagequestion'), ('add_question', 'Can add question'), ('change_question', 'Can change question'), ('delete_question', 'Can delete question'), ('view_question', 'View question'))},
        ),
        migrations.AlterModelOptions(
            name='multiplechoiceanswer',
            options={'permissions': (('view_multiplechoiceanswer', 'View multiplechoiceanswer'), ('add_answer', 'Can add answer'), ('change_answer', 'Can change answer'), ('delete_answer', 'Can delete answer'), ('view_answer', 'View answer'))},
        ),
        migrations.AlterModelOptions(
            name='multiplechoicequestion',
            options={'permissions': (('view_multiplechoicequestion', 'View multiplechoicequestion'), ('add_question', 'Can add question'), ('change_question', 'Can change question'), ('delete_question', 'Can delete question'), ('view_question', 'View question'))},
        ),
        migrations.AlterModelOptions(
            name='textanswer',
            options={'permissions': (('view_textanswer', 'View textanswer'), ('add_answer', 'Can add answer'), ('change_answer', 'Can change answer'), ('delete_answer', 'Can delete answer'), ('view_answer', 'View answer'))},
        ),
        migrations.AlterModelOptions(
            name='textquestion',
            options={'permissions': (('view_textquestion', 'View textquestion'), ('add_question', 'Can add question'), ('change_question', 'Can change question'), ('delete_question', 'Can delete question'), ('view_question', 'View question'))},
        ),
    ]
