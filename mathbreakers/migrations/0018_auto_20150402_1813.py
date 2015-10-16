# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathbreakers', '0017_classroomlog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CampSignup',
        ),
        migrations.RemoveField(
            model_name='emailreferral',
            name='sender',
        ),
        migrations.DeleteModel(
            name='EmailReferral',
        ),
        migrations.RemoveField(
            model_name='lessonplan',
            name='cclessons',
        ),
        migrations.RemoveField(
            model_name='lessonplan',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='userlessonplanpurchase',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='userlessonplanpurchase',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserLessonPlanPurchase',
        ),
        migrations.DeleteModel(
            name='VirtualHug',
        ),
        migrations.RemoveField(
            model_name='levelgroup',
            name='lesson_plan',
        ),
        migrations.DeleteModel(
            name='LessonPlan',
        ),
    ]
