# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0006_fulldownloadcodeemailentry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='num',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='teachersignupflow',
            name='max_level_reached',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='teachersignupflow',
            name='median_level_reached',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='teachersignupflow',
            name='median_playtime',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
    ]
