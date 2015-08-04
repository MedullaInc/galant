# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0005_auto_20150728_0854'),
        ('quotes', '0008_auto_20150803_1240'),
        ('briefs', '0026_auto_20150803_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='brief',
            name='client',
            field=models.ForeignKey(default=1, to='gallant.Client'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brief',
            name='quote',
            field=models.ForeignKey(to='quotes.Quote', null=True),
        ),
    ]
