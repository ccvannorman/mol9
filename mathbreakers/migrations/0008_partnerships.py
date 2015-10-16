# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0007_auto_20150308_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partnerships',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization', models.CharField(max_length=256, null=True, blank=True)),
                ('our_contact', models.CharField(max_length=256, null=True, blank=True)),
                ('estimated_reach', models.CharField(max_length=256, null=True, blank=True)),
                ('wholesale_price', models.CharField(max_length=128, null=True, blank=True)),
                ('retail_price', models.CharField(max_length=128, null=True, blank=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('remarks', models.CharField(max_length=2048, null=True, blank=True)),
                ('tracking_cookie', models.CharField(max_length=256)),
                ('start', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
