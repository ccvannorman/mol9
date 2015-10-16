# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ButtonLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('ip', models.IPAddressField(null=True, blank=True)),
                ('time', models.DateTimeField()),
                ('tracking_cookie', models.CharField(max_length=256, null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CampSignup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parent_name', models.CharField(max_length=256)),
                ('parent_email', models.EmailField(max_length=256)),
                ('child_name', models.CharField(max_length=256)),
                ('child_age', models.IntegerField()),
                ('session', models.IntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('plus_kit', models.BooleanField(default=False)),
                ('purchaseid', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CCLesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=4096)),
                ('short_description', models.CharField(max_length=128)),
                ('mb', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CCLessonCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CCLessonGrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('number', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gems', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('school', models.CharField(max_length=512)),
                ('grade', models.CharField(max_length=64)),
                ('num_students', models.IntegerField()),
                ('activated', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClassroomActivityBin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_seconds', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('classroom', models.ForeignKey(to='mathbreakers.Classroom')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClassroomSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=64)),
                ('start_time', models.DateTimeField()),
                ('update_time', models.DateTimeField(null=True, blank=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('ip', models.IPAddressField()),
                ('tracking_cookie', models.CharField(max_length=256, null=True, blank=True)),
                ('classroom', models.ForeignKey(blank=True, to='mathbreakers.Classroom', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClassroomTeacherRel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('classroom', models.ForeignKey(to='mathbreakers.Classroom')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CohortTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tracking_cookie', models.CharField(max_length=256)),
                ('cohort', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EducationTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailReferral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('code', models.CharField(max_length=128)),
                ('clicked', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('total', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailSurveyResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('response', models.CharField(max_length=1024)),
                ('post_answer_message_title', models.CharField(max_length=1024)),
                ('post_answer_message_description', models.CharField(max_length=1024, null=True, blank=True)),
                ('num', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_file', models.FileField(default=b'', upload_to=b'uploads')),
                ('gallery', models.CharField(max_length=128)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameMenuClick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('button', models.CharField(max_length=256)),
                ('time', models.DateTimeField()),
                ('click_type', models.IntegerField()),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GamePurchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deluxe', models.BooleanField(default=False)),
                ('time', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GamePurchaseEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('time', models.DateTimeField()),
                ('code', models.CharField(max_length=256)),
                ('downloads', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HeatmapPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('point_x', models.FloatField()),
                ('point_y', models.FloatField()),
                ('point_z', models.FloatField()),
                ('point_type', models.IntegerField()),
                ('level_name', models.CharField(max_length=1024)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_name', models.CharField(max_length=1024)),
                ('equipped', models.BooleanField(default=False)),
                ('variation', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KickstarterRedirect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('referrer', models.CharField(max_length=256)),
                ('num', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LessonPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=4096)),
                ('overview', models.CharField(max_length=4096)),
                ('instruction_time', models.IntegerField()),
                ('completion_time', models.IntegerField()),
                ('youtube_video_id', models.CharField(max_length=128)),
                ('pdf_url', models.CharField(max_length=4096)),
                ('upgrade_required', models.BooleanField(default=False)),
                ('cclessons', models.ManyToManyField(to='mathbreakers.CCLesson')),
                ('grade', models.ForeignKey(to='mathbreakers.CCLessonGrade')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=50)),
                ('picture', models.FileField(default=b'', null=True, upload_to=b'levels', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LevelGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('upgrade_required', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
                ('secret', models.BooleanField(default=False)),
                ('lesson_plan', models.ForeignKey(blank=True, to='mathbreakers.LessonPlan', null=True)),
                ('levels', models.ManyToManyField(to='mathbreakers.Level')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MathExperiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('desc', models.CharField(max_length=256)),
                ('picture', models.FileField(default=b'', null=True, upload_to=b'labs', blank=True)),
                ('url', models.CharField(max_length=512, null=True, blank=True)),
                ('future', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('code', models.CharField(max_length=1024)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PreorderRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=1024)),
                ('response', models.CharField(max_length=2048, null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchaseData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=256)),
                ('wallet_description', models.CharField(max_length=1024)),
                ('confirmation_description', models.CharField(max_length=1024)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('post_purchase_text', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchaseRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stripe_token', models.CharField(max_length=512)),
                ('email', models.EmailField(max_length=75)),
                ('code', models.CharField(max_length=512)),
                ('params', models.CharField(max_length=1024, null=True, blank=True)),
                ('price', models.IntegerField()),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoboterraLogin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField(null=True, blank=True)),
                ('time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RobotSentEmail',
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
        migrations.CreateModel(
            name='SUTeacherNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tracking_cookie', models.CharField(max_length=256)),
                ('column', models.CharField(max_length=256)),
                ('checked', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeacherSignupFlow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tracking_cookie', models.CharField(max_length=256)),
                ('start', models.DateTimeField(null=True, blank=True)),
                ('order', models.IntegerField(default=0)),
                ('cohort', models.CharField(max_length=256, null=True, blank=True)),
                ('cohort_color', models.CharField(max_length=16, null=True, blank=True)),
                ('started_cohort', models.BooleanField(default=False)),
                ('clicked_teacher_start', models.BooleanField(default=False)),
                ('btn1_count', models.IntegerField(default=0)),
                ('clicked_start_session', models.BooleanField(default=False)),
                ('session_started', models.BooleanField(default=False)),
                ('classroom_name', models.CharField(max_length=256, null=True, blank=True)),
                ('username', models.CharField(max_length=256, null=True, blank=True)),
                ('has_students', models.BooleanField(default=False)),
                ('num_students', models.IntegerField(default=0)),
                ('num_students_created_manually', models.IntegerField(default=0)),
                ('has_playtime', models.BooleanField(default=False)),
                ('playtime', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('second_visit', models.BooleanField(default=False)),
                ('num_visits', models.IntegerField(default=0)),
                ('pressed_purchase_nav', models.BooleanField(default=False)),
                ('pressed_purchase_timer', models.BooleanField(default=False)),
                ('purchased', models.BooleanField(default=False)),
                ('purchase_price', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeacherWaitlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('school', models.CharField(max_length=256, null=True, blank=True)),
                ('how_hear', models.CharField(max_length=256, null=True, blank=True)),
                ('firstname', models.CharField(max_length=64, null=True, blank=True)),
                ('lastname', models.CharField(max_length=64, null=True, blank=True)),
                ('study', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=16, null=True, blank=True)),
                ('num_students', models.IntegerField()),
                ('email', models.CharField(max_length=128)),
                ('date', models.DateTimeField()),
                ('convertedToCohort', models.BooleanField(default=False)),
                ('cohort', models.CharField(max_length=128, null=True, blank=True)),
                ('num_emails_sent', models.IntegerField(null=True, blank=True)),
                ('last_email_sent', models.CharField(max_length=128, null=True, blank=True)),
                ('last_email_sent_date', models.DateTimeField(null=True, blank=True)),
                ('total_communication_log', models.CharField(max_length=4096, null=True, blank=True)),
                ('AB_test_description', models.CharField(max_length=4096, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TryLater',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('time', models.DateTimeField()),
                ('ip', models.IPAddressField()),
                ('schedule_support', models.BooleanField(default=False)),
                ('schedule_play', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAdaptiveSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skill_id', models.CharField(max_length=128)),
                ('skill_level', models.FloatField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserClassroomAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('classroom', models.ForeignKey(to='mathbreakers.Classroom')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLessonPlanPurchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan', models.ForeignKey(to='mathbreakers.LessonPlan')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLevelState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False)),
                ('stars', models.IntegerField()),
                ('assigned', models.BooleanField(default=False)),
                ('checkpoint', models.IntegerField(default=0)),
                ('level', models.ForeignKey(to='mathbreakers.Level')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upgraded', models.BooleanField(default=False)),
                ('send_news', models.BooleanField(default=False)),
                ('playtime', models.IntegerField(default=0)),
                ('teacher_of_classroom', models.ForeignKey(default=None, blank=True, to='mathbreakers.Classroom', null=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserTopicState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mastery', models.FloatField()),
                ('attempts', models.IntegerField()),
                ('correct', models.IntegerField()),
                ('topic', models.ForeignKey(to='mathbreakers.EducationTopic')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VirtualHug',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('referral', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='emailsurvey',
            name='responses',
            field=models.ManyToManyField(to='mathbreakers.EmailSurveyResponse'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cclesson',
            name='category',
            field=models.ForeignKey(to='mathbreakers.CCLessonCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cclesson',
            name='grade',
            field=models.ForeignKey(to='mathbreakers.CCLessonGrade'),
            preserve_default=True,
        ),
    ]
