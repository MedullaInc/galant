# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_auto_20150804_1349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quote',
            options={'permissions': (('view_quote', 'View quote'),)},
        ),
        migrations.AlterModelOptions(
            name='quotetemplate',
            options={'permissions': (('view_quotetemplate', 'View quotetemplate'),)},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'permissions': (('view_section', 'View section'),)},
        ),
        migrations.AlterModelOptions(
            name='servicesection',
            options={'permissions': (('view_servicesection', 'View servicesection'),)},
        ),
        migrations.AlterModelOptions(
            name='textsection',
            options={'permissions': (('view_textsection', 'View textsection'),)},
        ),
    ]
