# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0004_auto_20150807_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('address', models.CharField(max_length=255)),
                ('address_2', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=127)),
                ('state', models.CharField(max_length=127)),
                ('zip', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(regex=b'^\\d{5}(?:[-\\s]\\d{4})?$', message=b"Zipcode must be entered in the format: '12345-1234' (first five digits required).")])),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='gallantuser',
            name='company_name',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='gallantuser',
            name='name',
            field=models.CharField(default='John Doe', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gallantuser',
            name='contact_info',
            field=models.ForeignKey(to='gallant.ContactInfo', null=True),
        ),
    ]
