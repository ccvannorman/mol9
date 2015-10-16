# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0002_userprofile_upgrade_num_licenses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='upgrade_num_licenses',
            new_name='num_licenses',
        ),
    ]
