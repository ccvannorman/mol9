# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0005_fulldownloadcodeemailentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='fulldownloadcodeemailentry',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 4, 18, 32, 57, 966000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
