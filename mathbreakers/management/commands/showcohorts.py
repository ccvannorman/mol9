from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
import random
from django.core.mail import send_mail


class Cohorts(object):
    def __init__(self, letter, teacherCount, last_email_sent, last_email_sent_date,total_communication_log,AB_test_description,num_students):
	self.letter = letter
	self.teacherCount = teacherCount
	self.studentCount = num_students
	self.last_email_sent = last_email_sent
	self.last_email_sent_date = last_email_sent_date
	self.total_communication_log = total_communication_log
	self.AB_test_description = AB_test_description



class Command(BaseCommand):


	args = ''
	help = 'returns the cohorts with num teachers, letter, and last touch info'
	def handle(self, verbose=None, *args, **options):
		l = list(TeacherWaitlist.objects.exclude(cohort=""))
		verbose = (verbose == "verbose") or (verbose == True) 
		cohortList = []
		for item in l:
			# if any(c.letter = item.cohort for c in cohortList):
			found = False
			for c in cohortList:
				if c.letter == item.cohort:
					c.teacherCount += 1
					found = True
					c.studentCount += item.num_students
			if verbose:
				print 'email: ' + item.email
				print 'students: ' + item.num_students
			if False == found:
				cohortList.append(
					Cohorts(
						item.cohort,
						1,
						item.last_email_sent,
						item.last_email_sent_date,
						item.total_communication_log,
						item.AB_test_description,
						item.num_students))
		print ""
		print ""	
		print "Found " + str(len(cohortList)) + " cohorts."
		cohortList = sorted(cohortList, key=lambda self : self.letter)
		for c in cohortList[:]:
			print str(c.letter)
			print " " + str(c.teacherCount) + " teachers "
			print " " + str(c.studentCount) + " students "
			print " " + str(c.studentCount / c.teacherCount) + " students per teacher"
			print " last email sent: "+str(c.last_email_sent_date)
			print " : "+str(c.last_email_sent)[:40].strip('\n\r\t')

		print ""
		print ""


