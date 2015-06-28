# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0003_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=0, max_length=2, choices=[(b'5', b'ACCEPTED'), (b'0', b'DRAFT'), (b'1', b'NOT_SENT'), (b'6', b'REJECTED'), (b'2', b'SENT'), (b'4', b'SUPERSEDED'), (b'3', b'VIEWED')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(help_text=b'For emailing URL', max_length=64, unique=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceSection',
            fields=[
                ('section_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='quotes.Section')),
                ('service', models.ForeignKey(to='gallant.Service')),
            ],
            bases=('quotes.section',),
        ),
        migrations.AddField(
            model_name='section',
            name='parent',
            field=models.ForeignKey(related_name='sub_sections', blank=True, to='quotes.Section', null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='text',
            field=models.ForeignKey(related_name='text', to='gallant.ULText'),
        ),
        migrations.AddField(
            model_name='section',
            name='title',
            field=models.ForeignKey(related_name='title', to='gallant.ULText'),
        ),
        migrations.AddField(
            model_name='quote',
            name='intro',
            field=models.ForeignKey(related_name='intro', to='quotes.Section', null=True),
        ),
        migrations.AddField(
            model_name='quote',
            name='notes',
            field=models.ForeignKey(related_name='notes', to='quotes.Section', null=True),
        ),
        migrations.AddField(
            model_name='quote',
            name='parent',
            field=models.ForeignKey(related_name='versions', blank=True, to='quotes.Quote', null=True),
        ),
        migrations.AddField(
            model_name='quote',
            name='sections',
            field=models.ManyToManyField(to='quotes.Section', blank=True),
        ),
    ]
