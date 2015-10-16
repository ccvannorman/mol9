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

class Command(BaseCommand):
	args = ''
	help = 'Updates the teacher flow models'

	def handle(self, *args, **options):	

		print "Calculating cohorts"
		# Get all the cohorts we know about
		cohort_set = set([v['cohort'] for v in list(CohortTracking.objects.values("cohort"))])
		# Make them into the dictionary format cohort_name:index
		cohorts = {b:a for a,b in enumerate(cohort_set)}
		teachers = {}
		print "Finding first clicks"
		btn_click_counts = ButtonLog.objects.filter(name="teacherclick1").values_list('tracking_cookie', flat=True).annotate(click_count=Count('tracking_cookie')).values_list('tracking_cookie', 'click_count')
		btn_click_counts = {k:v for k,v in btn_click_counts}

		email_cohorts = {tw.email:tw.cohort for tw in TeacherWaitlist.objects.all()}

		for log in ButtonLog.objects.filter(name="teacherclick1").values('tracking_cookie').distinct().values('tracking_cookie', 'time'):
			tc = log['tracking_cookie']
			t = {
				"start":log['time'].astimezone(pytz.timezone("US/Pacific")),
				"btn1_count":btn_click_counts[tc],
				"tracking_cookie":tc,
				"clicked_teacher_start":True,
				"order":1}

			teachers[tc] = t
		print len(teachers)

		print "Finding cohort start page views"
		for ct in CohortTracking.objects.all():
			tc = ct.tracking_cookie
			if teachers.has_key(tc):
				teachers[tc]["cohort"] = ct.cohort
				teachers[tc]["started_cohort"] = True
			else:
				t = {
					"tracking_cookie":tc,
					"started_cohort":True,
					"cohort":ct.cohort,
					"order":1}
				teachers[tc] = t
		print len(teachers)

		print "Finding session starts"
		for log in ButtonLog.objects.filter(name="startSession"):
			tc = log.tracking_cookie
			if teachers.has_key(tc):
				teachers[tc]["clicked_start_session"] = True
				teachers[tc]["order"] = 2
			else:
				t = {
				"start":log.time.astimezone(pytz.timezone("US/Pacific")),
				"tracking_cookie":tc,
				"clicked_start_session":True,
				"order":2}
				teachers[tc] = t
		print len(teachers)

		print "Preparing classroom details cache"
		ctrs = {ctr.classroom:ctr.user for ctr in ClassroomTeacherRel.objects.all()}
		classroom_students = UserClassroomAssignment.objects\
		.values_list("classroom__name",flat=True)\
		.annotate(student_count=Count('classroom__name'))\
		.values_list("classroom__name", "student_count")
		classroom_students = {k:v for k,v in classroom_students}

		classroom_playtime = ClassroomActivityBin.objects\
		.values('classroom__name').order_by('classroom__name')\
		.annotate(total_seconds=Sum('num_seconds'))\
		.values_list('classroom__name','num_seconds')
		classroom_playtime = {k:v for k,v in classroom_playtime}

		classroom_max_level = Classroom.objects.values('name')\
		.filter(userclassroomassignment__user__userlevelstate__completed=True)\
		.annotate(max_level=models.Max('userclassroomassignment__user__userlevelstate__level__num'))\
		.values_list('name','max_level')
		classroom_max_level = {k:v for k,v in classroom_max_level}

		classroom_sum_level = Classroom.objects.values('name')\
		.filter(userclassroomassignment__user__userlevelstate__completed=True)\
		.annotate(sum_level=models.Sum('userclassroomassignment__user__userlevelstate__level__num'))\
		.values_list('name','sum_level')
		classroom_sum_level = {k:v for k,v in classroom_sum_level}	

		print "Processing classroom details"
		for sess in ClassroomSession.objects.all():
			tc = sess.tracking_cookie
			if teachers.has_key(tc):
				mt = teachers[tc]
				mt["session_started"] = True
				mt["classroom_name"] = sess.classroom.name
				mt["order"] = 3

				user = ctrs[sess.classroom]
				if email_cohorts.has_key(user.email):
					mt["cohort"] = email_cohorts[user.email]
				mt["username"] = user.username
				ns = mt.get("num_students", 0)
				ns += classroom_students.get(sess.classroom.name, 0)
				mt["num_students"] = ns
				mt["has_students"] = classroom_students.has_key(sess.classroom.name) or mt.get("has_students", False)
				if mt["has_students"]:
					mt["order"] = 6
				pprice = sum([p.price for p in user.purchaserecord_set.filter(code="teacherpurchase")]) / 100.0
				mt["purchase_price"] = "%.2f" % pprice
				mt["purchased"] = user.profile.upgraded or (pprice > 0)

				mt["max_level_reached"] = max(
					classroom_max_level.get(sess.classroom.name, 0), 
					mt.get("max_level_reached", 0))

				mt["sum_level_reached"] = classroom_sum_level.get(sess.classroom.name, 0) + mt.get("sum_level_reached", 0)				

				playtime = mt.get("playtime", 0)
				playtime += classroom_playtime.get(sess.classroom.name,0) / 60

				
				mt["has_playtime"] = playtime > 0
				if mt["has_playtime"]:
					mt["order"] = 7
				mt["playtime"] = playtime
				#if mt["purchased"]:
					#mt["order"] = 100

		print "Discovering 'manage class' clicks"
		add_click_counts = ButtonLog.objects.filter(name="createStudent").values_list('tracking_cookie', flat=True).annotate(click_count=Count('tracking_cookie')).values_list('tracking_cookie', 'click_count')
		add_click_counts = {k:v for k,v in add_click_counts}		
		for log in ButtonLog.objects.filter(name="createStudent"):
			tc = log.tracking_cookie
			if teachers.has_key(tc):
				teachers[tc]["num_students_created_manually"] = add_click_counts.get(tc, 0)

		print "Getting details about purchase clicks"
		for log in ButtonLog.objects.filter(name="license"):
			tc = log.tracking_cookie
			if teachers.has_key(tc):
				teachers[tc]["pressed_purchase_nav"] = True
				teachers[tc]["order"] = max(teachers[tc]["order"], 5)

		for log in ButtonLog.objects.filter(name="teacherbuy"):
			tc = log.tracking_cookie
			if teachers.has_key(tc):
				teachers[tc]["pressed_purchase_timer"] = True
				teachers[tc]["order"] = max(teachers[tc]["order"], 5)

		print "Getting details about second visits"
		
		pick_cts = dupe_count_as_dict(ButtonLog.objects.filter(name="picklobby"), "tracking_cookie")
		for log in ButtonLog.objects.filter(name="picklobby"):
			tc = log.tracking_cookie
			if teachers.has_key(tc):
				teachers[tc]["order"] = max(teachers[tc]["order"], 4)
				teachers[tc]["second_visit"] = True
				teachers[tc]["num_visits"] = pick_cts.get(tc, 0)

		print "Deleting old teacher flow objects"
		TeacherSignupFlow.objects.all().delete()

		print "Adding new teacher flow objects"
		num = 0
		for t in teachers.values():
			if t["tracking_cookie"] is not None and (t.get("has_playtime",False) or t.has_key("start") or t.has_key("session_started")):
				num += 1
				tsf = TeacherSignupFlow(**t)
				tsf.save()
		print "Wrote " + str(num) + " teacher flow objects to DB"
