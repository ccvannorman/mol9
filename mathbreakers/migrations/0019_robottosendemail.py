# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0018_auto_20150402_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='RobotToSendEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('title', models.CharField(max_length=1024)),
                ('content', models.CharField(max_length=10000)),
                ('time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
