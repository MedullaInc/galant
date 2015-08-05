# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0002_auto_20150804_1349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'permissions': (('view_client', 'View client'),)},
        ),
        migrations.AlterModelOptions(
            name='note',
            options={'permissions': (('view_note', 'View note'),)},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('view_project', 'View project'),)},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'permissions': (('view_service', 'View service'),)},
        ),
    ]
