# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0015_userprofile_unlimited_licenses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasedata',
            name='confirmation_description',
        ),
        migrations.RemoveField(
            model_name='purchasedata',
            name='post_purchase_text',
        ),
        migrations.RemoveField(
            model_name='purchasedata',
            name='wallet_description',
        ),
    ]
