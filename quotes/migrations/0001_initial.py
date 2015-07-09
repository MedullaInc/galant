# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallant.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'New Quote', max_length=512)),
                ('language', models.CharField(help_text=b'Language of quote, or null for template.', max_length=7, null=True, choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('status', models.CharField(default=0, max_length=2, choices=[(b'5', b'Accepted'), (b'0', b'Draft'), (b'1', b'Not_Sent'), (b'6', b'Rejected'), (b'2', b'Sent'), (b'4', b'Superseded'), (b'3', b'Viewed')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(help_text=b'For emailing URL', max_length=64, unique=True, null=True)),
                ('client', models.ForeignKey(to='gallant.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', gallant.fields.ULCharField()),
                ('text', gallant.fields.ULTextField()),
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
