from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
from django.conf import settings
import datetime
from mathbreakers import mbcopy
from mathbreakers.util import *
from django.utils import timezone
from mathbreakers.session import *
from django.utils import timezone
from mathbreakers.queries import *

class Command(BaseCommand):

	args = ''
	help = """

		'emails the appropriate trickle to some databased peoples' 
	

		"""
	def handle(self, dryrun=False, *args, **options):
		dryrun = dryrun == "dryrun"
		numEmailedWithSomeLicenses = 0
		numEmailedWithNoLicenses = 0
		teachers = get_all_teachers_classrooms()
		print len(teachers)
		for to in teachers:
			t = timezone.now() + datetime.timedelta(days=7)			
			duedate = t.strftime("%A, %B %d")
			name = ''
			s = ""
			m = ""  

			user = to["user"]
	
			if not TeacherWaitlist.objects.filter(email=user.email).exists():
				print 'email doesnt exist!: ' + user.email
				continue
			name = TeacherWaitlist.objects.get(email=user.email).firstname
			diff = 0
			# print value["email"] + " had "+ str(value["num_licenses"]) + " wit h " + str(value["num_students"]) + " students. total playtime was : " + str(value["total_playtime"]) + "; total students was : " + str(value["num_students"])
			if name == "": 
				name = "Hello"
			if to["total_students"] == 0:
				print user.email + " was not ready, total students == 0."
				continue
			elif to["total_playtime"] <= 20:
				print user.email + " was not ready, total playtime <= 20."
				continue
			elif user.profile.num_licenses == 0 and to["total_students"] > 0:
				s = mbcopy.TEACHER_STARTED_NOT_PURCHASED_YET[0]
				m = mbcopy.TEACHER_STARTED_NOT_PURCHASED_YET [1].format(name,duedate,"https://mathbreakers.com/teacher/purchase")
				# print value["email"] + " had no licenses but " + str(value["num_students"]) + " students."
			elif to["total_students"] * 30 > to["total_playtime"]:
				s = mbcopy.TEACHER_TIME_HALF_UP_INSUFFICIENT_LICENSES[0]
				diff = to["total_students"] - user.profile.num_licenses
				m = mbcopy.TEACHER_TIME_HALF_UP_INSUFFICIENT_LICENSES[1].format(
					name,
					user.profile.num_licenses,
					to["total_students"],
					diff,
					diff*3)
				if diff <= 0:
					m = ""
					s = ""
					print user.email + " already have more licenses than students)"
					continue
								
	
			if RobotSentEmail.objects.filter(title=s,email=user.email).exists():
				print user.email + 'was already emailed! with subject ' + s + ", skipping"
				continue
			elif m != "":
				ss = ' send to: ' + user.email + ": " + s + m[:20]
				ss = ss.replace('\n',' ').replace('\t',' ')
				# print ss
				# send_mail_sync(s,m,'charlie@mathbreakers.com',[value["email"]],True)
				if settings.REMOTEDB or dryrun:
					print user.email + " ___ will be skipped, because remotedb: " + str(settings.REMOTEDB) + "; dryrun : " + str(dryrun) 
				else:
					print "___LIVE:" + user.email + " is being emailed NOW! with: " + ss
					print user.email + " was update trial_to_expire to " + t
					user.profile.trial_to_expire = t
					user.save()
	
