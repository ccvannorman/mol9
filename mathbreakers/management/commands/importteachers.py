from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime

class Command(BaseCommand):
	args = 'None'
	help = 'imports teacher data from csv'
	
    	def handle(self, filename, *args, **options):
		f = open(filename)
		for line in f:
			school,how_hear,firstname,lastname,study,phone,num_students,email,dt,sentToCohort,cohortName = line.strip().split(",")
			struct = time.strptime(dt, "%m/%d/%Y %H:%M:%S")
			dt = datetime.datetime.fromtimestamp(time.mktime(struct))
			duedate = t.strftime("%A, %B %d")
			

			try:
				num_students = int(num_students)
			except: 
				num_students = 1
			study = study == "TRUE"
			
			newentry = TeacherWaitlist(school=school,
				how_hear=how_hear,
				firstname=firstname,
				lastname=lastname,
				study=study,
				num_students=num_students,
				email=email,
				date=dt,
				convertedToCohort=sentToCohort,
				cohort=cohortName,
				num_emails_sent=0)
			#	last_email_sent  models.CharField(max_length=128, null=True, blank=True)
#				last_email_sent_date = models.DateTimeField(null=True, blank=True)
#				total_communication_log = models.CharField(max_length=4096, null=True, blank=True)
#				AB_test_description = models.CharField(max_length=4096, null=True, blank=True)
#				sent_halfway_email = models.BooleanField(default=False)

			newentry.save()
		
		f.close()
