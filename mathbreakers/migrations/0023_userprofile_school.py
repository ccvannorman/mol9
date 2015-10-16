# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0022_auto_20150721_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='school',
            field=models.CharField(default=b'', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
