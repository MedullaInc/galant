# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid

def gen_uuid(apps, schema_editor): # pragma: no cover
    MyModel = apps.get_model('briefs', 'Brief')
    for row in MyModel.objects.all():
        row.token = uuid.uuid4()
        row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('briefs', '0014_auto_20150801_1156'),
    ]

    operations = [
        migrations.RunPython(gen_uuid),
    ]
