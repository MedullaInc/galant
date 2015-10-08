# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gallant', '0018_auto_20150916_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_by_parent', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField(auto_now_add=True)),
                ('daily_estimate', models.DecimalField(default=0.0, help_text=b'Time estimate in hours per day', max_digits=3, decimal_places=1, blank=True)),
                ('assignee', models.ForeignKey(related_name='assignee', to=settings.AUTH_USER_MODEL)),
                ('notes', models.ManyToManyField(to='gallant.Note')),
                ('project', models.ForeignKey(blank=True, to='gallant.Project', null=True)),
                ('services', models.ManyToManyField(to='gallant.Service')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_task', 'View task'),),
            },
        ),
    ]
