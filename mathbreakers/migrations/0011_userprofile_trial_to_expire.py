# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0010_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='trial_to_expire',
            field=models.DateTimeField(default=None, null=True),
            preserve_default=True,
        ),
    ]
