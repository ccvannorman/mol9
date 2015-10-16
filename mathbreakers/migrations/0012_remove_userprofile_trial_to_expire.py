# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0011_userprofile_trial_to_expire'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='trial_to_expire',
        ),
    ]
