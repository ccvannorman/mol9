# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0016_auto_20150330_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassroomLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=4096)),
                ('date', models.DateTimeField()),
                ('classroom', models.ForeignKey(to='mathbreakers.Classroom')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
