from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
import random
from django.core.mail import send_mail
from mathbreakers.queries import *
from django.utils import timezone

class Command(BaseCommand):
	args = ''
	help = 'migrating teachers with active playtime to TeacherWaitlist, if they arent already.'
	def handle(self, *args, **options):
		teachers = get_all_teachers_classrooms()
		num_skipped = 0
		num_migrated = 0
		for t in teachers:
			if TeacherWaitlist.objects.filter(email=t["user"].email):
				# print "[SKIP] already have "+t["user"].email
				num_skipped += 1
				continue
			else:
				num_migrated += 1
				feb1 = timezone.now() + datetime.timedelta(days=54)
				how_hear = ""
				cohortName = ""
				if feb1 < t["user"].date_joined:
					print t["user"].email + " joined before feb 1. " + str(t["user"].date_joined) + "-__ diff"
					how_hear = "From old system"
					cohortName = "OLD"
				else:
					print t["user"].email + " joine dafter feb 1: " + str(t["user"].date_joined)
					how_hear = "Organic since feb 1 launch"
					cohortName = "Organic"
				#struct = time.strptime(dt, "%m/%d/%Y %H:%M:%S")
				#dt = datetime.datetime.fromtimestamp(time.mktime(struct))
				#duedate = t.strftime("%A, %B %d")
				school = t["user"].email.split("@")[1].split(".")[0] # pull the "school" from "teacher@school.com"
				num_students = t["total_students"]
				newentry = TeacherWaitlist(
					school = school,
					how_hear = how_hear,
					firstname = "",
					lastname = "",
					study = False,
					num_students = t["total_students"],
					email = t["user"].email,
					date = t["user"].date_joined,
					convertedToCohort = "",
					cohort = cohortName,
					)
				print "  __newentry: " + str(t["user"].email)
				newentry.save()
				
			
		print "num skipped: " + str(num_skipped)
		print "num migrated and saved; " + str(num_migrated)	
