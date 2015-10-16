# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mathbreakers', '0018_auto_20150402_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewInventoryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_type', models.CharField(max_length=256)),
                ('properties', models.CharField(max_length=4096)),
                ('equip_slot', models.CharField(max_length=256, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
