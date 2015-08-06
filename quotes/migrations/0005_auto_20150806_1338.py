# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_auto_20150805_2136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicesection',
            options={'permissions': (('view_servicesection', 'View servicesection'), ('add_section', 'Can add section'), ('change_section', 'Can change section'), ('delete_section', 'Can delete section'), ('view_section', 'View section'))},
        ),
        migrations.AlterModelOptions(
            name='textsection',
            options={'permissions': (('view_textsection', 'View textsection'), ('add_section', 'Can add section'), ('change_section', 'Can change section'), ('delete_section', 'Can delete section'), ('view_section', 'View section'))},
        ),
    ]
