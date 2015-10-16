from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
import random
from django.core.mail import send_mail
import sys
class Command(BaseCommand):

	args = ''
	help = 'clears the teacher table'
    	def handle(self,  *args, **options):
		question = "Really clear the cohorts? This will reset everthing.. is probably not a good idea if you're on the production server..."
		prompt = " [y/n] "
		choice = "n"
		while True:
			sys.stdout.write(question + prompt)
			choice = raw_input().lower()
			if choice == "y":
				print "ok buddy I hope you know what yer doin"
				excludethese = ["","first one"]

				l = list(TeacherWaitlist.objects.exclude(cohort__in=excludethese))
				for item in l:
					item.cohort = ""
					item.last_email_sent=""
					item.last_email_sent_date=None
					item.total_communication_log=""
					item.AB_test_description = ""
					item.save()		
				print "removed all cohorts from table"
				return
			elif choic == "n":
				print "nothing deleted"
				return
			else:
			    sys.stdout.write("Please respond with 'yes' or 'no' "
					     "(or 'y' or 'n').\n")	
		print "your choice was: "+choice

