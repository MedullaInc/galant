# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0002_ultext'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parent', models.ForeignKey(related_name='sub_sections', blank=True, to='quotes.Section', null=True)),
                ('text', models.ForeignKey(related_name='text', to='gallant.ULText')),
                ('title', models.ForeignKey(related_name='title', to='gallant.ULText')),
            ],
        ),
        migrations.AddField(
            model_name='quote',
            name='intro',
            field=models.ForeignKey(to='quotes.Section'),
        ),
    ]
