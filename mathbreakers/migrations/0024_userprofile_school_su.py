# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0023_userprofile_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='school_su',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
