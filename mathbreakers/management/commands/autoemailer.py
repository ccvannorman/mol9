from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
from mathbreakers import mbcopy
from mathbreakers.util import *
from django.utils import timezone
from mathbreakers.queries import get_all_teachers_classrooms

class Command(BaseCommand):

	args = ''
	help = 'emails the appropriate trickle to some databased peoples'
	def handle(self, dryrun=False, *args, **options):
		dryrun = "dryrun" == dryrun
		message = ""
		subject = ""
		numEmailedWithSomeLicenses = 0
		numEmailedWithNoLicenses = 0
		teachers = get_all_teachers_classrooms()
		num_skipped = 0
		num_emailed = 0
		for item in teachers:
			# print item["user"].email + " had no licenses but " + str(item["total_students"]) + " students."
			name = ''
			s = ""
			m = ""  
			playtime_per_student = 0
			if not item["total_students"] == 0:
				playtime_per_student = truncate(item["total_playtime"] / item["total_students"], 2)
			if not TeacherWaitlist.objects.filter(email=item["user"].email).exists():
				# print 'SKIP .. email doesnt exist: ' + item["user"].email
				num_skipped += 1
				continue
			if TeacherWaitlist.objects.get(email=item["user"].email).cohort == "":
				# print 'SKIP: .. email not associated with cohort yet: ' + item["user"].email
				num_skipped += 1
				continue
			name = TeacherWaitlist.objects.get(email=item["user"].email).firstname
			if name == "": 
				name = "Hello"
			if item["total_playtime"] == 0:
				s = mbcopy.TEACHER_STARTED_NO_STUDENTS_YET[0]
				m = mbcopy.TEACHER_STARTED_NO_STUDENTS_YET[1].format(name)
			elif item["user"].profile.num_licenses == 0 and item["total_students"] > 0:
				s = mbcopy.TEACHER_STARTED_NOT_PURCHASED_YET[0]
				m = mbcopy.TEACHER_STARTED_NOT_PURCHASED_YET [1].format(name,"https://mathbreakers.com/teacher/purchase")
			elif item["total_students"] > item["user"].profile.num_licenses and item["user"].profile.num_licenses > 0:
				s = mbcopy.TEACHER_TIME_HALF_UP_INSUFFICIENT_LICENSES[0]
				diff = item["total_students"] - item["user"].profile.num_licenses
				m = mbcopy.TEACHER_TIME_HALF_UP_INSUFFICIENT_LICENSES[1].format(
					name,
					item["user"].profile.num_licenses,
					item["total_students"],
					diff,
					diff*3)
				# print item["user"].email + " had "+ str(item["user"].profile.num_licenses) + " wit h " + str(item["total_students"]) + " students. total playtime was : " + str(value["total_playtime"]) + "; total students was : " + str(item["total_students"])
	
			if RobotSentEmail.objects.filter(title=s,email=item["user"].email).exists():
				# print 'SKIP: .. robot already sent email to ' + item["user"].email + ' with subject ' + s + ", skipping"
				num_skipped += 1
				continue
			elif s == "": 
				# print "SKIP: .. not ready for email: " + item["user"].email + " .. totalstudents: " + str(item["total_students"]) + ", playtime per: " + str(playtime_per_student) + ", licenses bought : " + str(item["user"].profile.num_licenses)
				num_skipped += 1
				continue
			else:
				ss = 'emailed: ' + item["user"].email + ": " + s + m[:4] + ".." + " .. totalstudents: " + str(item["total_students"]) + ", playtime per: " + str(playtime_per_student) + ", licenses bought : " + str(item["user"].profile.num_licenses)
				num_emailed += 1
				ss = ss.replace('\n',' ').replace('\t',' ')
				# print ss
				if not dryrun:
					time.sleep(1)
					send_mail_sync(s,m,'charlie@mathbreakers.com',[item["user"].email])
				else:
					print "dryrun: " + item["user"].email + " message: " + ss
		print "emailed " + str(num_emailed) + ", skipped " + str(num_skipped)
