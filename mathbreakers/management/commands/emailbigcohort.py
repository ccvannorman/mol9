from mathbreakers.settings import REMOTEDB
from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
from mathbreakers import mbcopy
from mathbreakers.util import *
from django.utils import timezone
from mathbreakers.models import *

class Command(BaseCommand):

	args = ''
	help = 'emails the appropriate trickle to some databased peoples'
	def handle(self, selectedCohort=None, emailNo=0,  dryrun="", *args, **options):
		sent_emails = 0
		dryrun = dryrun == "dryrun"
		if selectedCohort is None or emailNo == 0: 
			print 'usage: emailcohort  [cohort A,B..]  [email # 1, 2, 3..]  [ABtest "testA","testB"], [dryrun (optional)]'
			return
		if not TeacherWaitlist.objects.filter(cohort = selectedCohort).exists():
			print 'cohort doesn\'t exist, exiting!'
			return
		emailNo = int(emailNo)		
		ABTestUrl = "mathbreakers.com/start/" + selectedCohort + "/"

		message = ""
		subject = "" 
		numSkipped = 0;
		for item in TeacherWaitlist.objects.filter(cohort = selectedCohort):
			if ClassroomTeacherRel.objects.filter(user__username = item.email).exists():
				print "SKIP: .. this teacher already started a classroom, "
				numSkipped += 1;
				continue
			#if item.num_emails_sent >= emailNo:
			#	print 'too many emails sent to this teacher already, exiting --'
			#	return
			if emailNo == 1:
				subject = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_BIG_1[0].format(item.firstname)
				message = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_BIG_1[1].format(item.firstname,item.num_students,ABTestUrl)
#			#elif emailNo == 2:
#				subject = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_2[0].format(item.firstname)
#				message = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_2[1].format(item.firstname,ABTestUrl)
#			elif emailNo == 3:
#				subject = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_3[0].format()
#				message = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_3[1].format(item.firstname,ABTestUrl)
			else:
				print 'something went wrong and no email was sent: ' + item.email
				return
			s = 0
			#for item2 in RobotSentEmail.objects.all():
		#		s += 1
	#			if s > 10:
#					break
#				print "robot item: " + str(item2.email)
			if RobotSentEmail.objects.filter(title = subject): #, email = item.email).exists():
				print 'SKIP: .. robotsentemails already has a record of this: ' + item.email
				numSkipped += 1
				continue
			# print 'just sent an email to ' + item.email	
			#update item with new info
			item.num_emails_sent = int(int(item.num_emails_sent) + 1)
			item.last_email_sent = subject + message
			item.last_email_sent_date = timezone.now()
			if item.total_communication_log == None: 
				item.total_communication_log = subject + message
			else:
				item.total_communication_log = item.total_communication_log + subject + message
			if not dryrun and not REMOTEDB:
				time.sleep( 1 )
				item.save()
				send_mail_sync(subject, message, 'charlie@mathbreakers.com', [item.email])
				sent_emails += 1
			else:
				print "[Skip] [Dryrun:" + str(dryrun) + "]  " + item.firstname + ", " + item.email
		sub = "Just sent " + str(sent_emails) + " emails " + "(skipped " + str(numSkipped) + ") of type "+str(emailNo)+" to teachers in cohort "+selectedCohort
		print "the email sent was:" + message
		if dryrun:
			 sub = "[dryrun]: " + sub
			#mes = """the last email sent was ..:
			#subject:""" + subject + """
			#""" + "body:" + message[:40] + "...." 
		print ""
		print ""
		print sub
		print ""
	#	send_mail_sync(sub,mes,"robot@mathbreakers.com",["team@mathbreakers.com"])
		

