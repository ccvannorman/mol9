from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers import session as mbsession
import uuid
import hashlib
from django.utils import timezone
from django.db.models import Count, Sum
import math
import pytz
from mathbreakers.queries import dupe_max, dupe_count_as_dict
from mathbreakers import analytics
import datetime

START_DATE = datetime.datetime(year=2015,month=1,day=1,hour=0,tzinfo=pytz.timezone("US/Pacific"))

class Command(BaseCommand):
	args = ''
	help = 'Sends mixpanel backdated events'

	def handle(self, *args, **options):	
		all_events = []

		vals = ClassroomSession.objects.filter(tracking_cookie__isnull=False).values("classroom__classroomteacherrel__user", "tracking_cookie")
		user_trackings = {v["classroom__classroomteacherrel__user"]:v["tracking_cookie"] for v in vals}


		def addevent(time, eventname, tracking):
			if time > START_DATE:
				eventname = "old_" + eventname
				all_events.append((time, eventname, tracking))

		def btnlog(btnname, evtname):
			for log in ButtonLog.objects.filter(name=btnname, time__gt=START_DATE).values('tracking_cookie').distinct().values('tracking_cookie', 'time'):
				time = log['time'].astimezone(pytz.timezone("US/Pacific"))
				addevent(time, evtname, log['tracking_cookie'])

		btnlog("teacherclick1", "visit_teacher_try")
		btnlog("visit", "visit_home")
		btnlog("license", "click_purchase_license_nav")
		btnlog("teacherbuy", "click_purchase_license_status")
		
		for ctr in ClassroomTeacherRel.objects.filter(date__gt=START_DATE):
			if user_trackings.has_key(ctr.user.id):
				time = ctr.date.astimezone(pytz.timezone("US/Pacific"))
				addevent(time, "post_teacher_start", user_trackings[ctr.user.id])

		print len(all_events)
		nameset = set([evt[1] for evt in all_events])
		print nameset
		#analytics.track_backdated_cookie_events(all_events)
