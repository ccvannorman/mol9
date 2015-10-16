# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0003_auto_20150227_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherwaitlist',
            name='sent_halfway_email',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
