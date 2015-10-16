# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0021_merge'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RobotToSendEmail',
        ),
        migrations.AddField(
            model_name='educentscode',
            name='date_claimed',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
