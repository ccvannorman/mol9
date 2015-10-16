# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0008_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teachersignupflow',
            old_name='median_level_reached',
            new_name='sum_level_reached',
        ),
    ]
