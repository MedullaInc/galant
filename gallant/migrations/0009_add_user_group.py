# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_user_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    GallantUser = apps.get_model('gallant', 'GallantUser')

    g = Group.objects.create(name='users')
    for u in GallantUser.objects.all():
        g.user_set.add(u)


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0008_auto_20150813_1253'),
    ]

    operations = [
        migrations.RunPython(add_user_group),
    ]
