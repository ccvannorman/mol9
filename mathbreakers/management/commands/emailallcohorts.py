from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
from mathbreakers import mbcopy
from mathbreakers.util import *
from django.utils import timezone
from mathbreakers.models import *
from mathbreakers.settings import REMOTEDB
from mathbreakers.queries import get_all_teachers_classrooms
from mathbreakers.settings_colors import bcolors

class Command(BaseCommand):

	args = ''
	help = 'emails the appropriate trickle to some databased peoples'
	def handle(self,  dryrun="", *args, **options):
		sent_emails = 0
		dryrun = dryrun == "dryrun"

		message = ""
		subject = "" 
		num_skipped = 0
		num_emailed = 0

		#emailed = []
		start_lobby_URL = "https://mathbreakers.com/start/N" # M was used week of Mar 20 - 27. N was used week of Mar 28 - Apr 6.
		daily_max = 100
		which_email = "none"
		for item in get_all_teachers_classrooms(): 
			if num_emailed >= daily_max:
				continue
			firstname = ""
			if TeacherWaitlist.objects.filter(email=item["user"].email).exists():
				firstname = TeacherWaitlist.objects.filter(email=item["user"].email)[0].firstname
			if firstname == "":
				firstname = "Hello"

			
			#  batch -- teachers with more students than licenses
			if item["user"].profile.num_licenses > 0 and item["user"].profile.num_licenses < item["total_students"]:
				subject = mbcopy.TEACHER_TIME_HALF_UP_INSUFFICIENT_LICENSES[0]
				message = mbcopy.TEACHER_TIME_HALF_UP_INSUFFICIENT_LICENSES[1].format(firstname,item["total_students"],item["user"].profile.num_licenses,item["total_students"]-item["user"].profile.num_licenses)
				which_email = "A"		
			#  batch -- teachers with all the licenses they need
			elif item["user"].profile.num_licenses > 0 and item["user"].profile.num_licenses >= item["total_students"]:
				subject = mbcopy.TEACHER_WITH_FULL_LICENSES[0]
				message = mbcopy.TEACHER_WITH_FULL_LICENSES[1].format(firstname)
				which_email = "B"
		
			#  batch -- teachers with an account but zero students
			elif item["total_students"] == 0:
				subject = mbcopy.TEACHER_STARTED_NO_STUDENTS_YET_2[0]
				message = mbcopy.TEACHER_STARTED_NO_STUDENTS_YET_2[1].format(firstname)
				which_email = "C"
		
			#  batch -- teachers with students but zero playtime
			elif item["total_playtime"] == 0:
				num_students = item["total_students"]
				subject = mbcopy.TEACHER_WITH_STUDENTS_ZERO_PLAYTIME[0]
				message = mbcopy.TEACHER_WITH_STUDENTS_ZERO_PLAYTIME[1].format(firstname,str(num_students) + " students")
				which_email = "D"
			now = timezone.now() + datetime.timedelta(days=-365) 
			lastTouched = now
			twoWeeksAgo = timezone.now() + datetime.timedelta(days=-14) 	
			twoMonthsAgo = timezone.now() + datetime.timedelta(days=-60) 	
			for ctr in ClassroomTeacherRel.objects.filter(user__email=item["user"].email):
				activities = ClassroomActivityBin.objects.filter(classroom=ctr.classroom)
				for activity in activities:
					# print "activity date for " + str(item["user"].email) + " w/ class:" + str(ctr.classroom) + " : " + str(activity.date)
					if lastTouched < activity.date:
						lastTouched = activity.date
			
			#  batch -- teachers with students with playtime, who have used the product in the past 2 weeks
			if lastTouched > twoWeeksAgo:
				subject = mbcopy.TEACHER_WITH_ACTIVITY_LAST_TWO_WEEKS[0] 
				message = mbcopy.TEACHER_WITH_ACTIVITY_LAST_TWO_WEEKS[1].format(firstname)
				which_email = "E"

			#  batch -- teachers with students with playtime, not for >2 weeks, but in the past 2 months
			elif lastTouched >= twoWeeksAgo and lastTouched < twoMonthsAgo:
				subject = mbcopy.TEACHER_WITH_NO_ACTIVITY_LAST_TWO_WEEKS[0]
				message = mbcopy.TEACHER_WITH_NO_ACTIVITY_LAST_TWO_WEEKS[1]  	
				which_email = "F"

			#  batch -- teachers with no playtime >2 months
			elif lastTouched >= twoMonthsAgo:
				subject = mbcopy.TEACHER_WITH_STUDENTS_NO_ACTIVITY_TWO_MONTHS[0]
				message = mbcopy.TEACHER_WITH_STUDENTS_NO_ACTIVITY_TWO_MONTHS[1].format(firstname,start_lobby_URL)  	
				which_email = "G"
			if RobotSentEmail.objects.filter(title = subject,email = item["user"].email).exists():
				print '[ SKIP ] : robot already sent ' + item["user"].email + " [ " + subject + " . . . ] which email: " + which_email
				num_skipped += 1
			elif not dryrun and not REMOTEDB:
				num_emailed += 1
				time.sleep(1)
				send_mail_sync(subject, message, 'charlie@mathbreakers.com', [item["user"].email])
			else:
				num_emailed += 1
				print "[dryrun/remoteDB] : [ " + which_email + " ] " + item["user"].email + "; " + subject 
		print ""
		print "num skipped: " + str(num_skipped)
		if dryrun or REMOTEDB:
			print "num dry emailed; " + str(num_emailed)
		else:
			print "num  emailed; " + str(num_emailed)
			
		


