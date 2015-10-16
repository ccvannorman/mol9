# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0013_unsubscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unsubscribed',
            name='email',
            field=models.CharField(max_length=256),
            preserve_default=True,
        ),
    ]
