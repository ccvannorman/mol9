# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0006_fulldownloadcodeemailentry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='date',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bug',
            name='level',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bug',
            name='position',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bug',
            name='session',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bug',
            name='user',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bug',
            name='vers',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bug',
            name='description',
            field=models.CharField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
    ]
