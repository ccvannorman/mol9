from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
import random
from django.utils import timezone
class Command(BaseCommand):
	args = 'cohort letter, cohort qty'
	help = 'selects 50 teachers and puts them into a cohort'
    	def handle(self, cohortName=None, fileName=None, *args, **options):
		if cohortName is None or fileName is None:
			print 'required usage: newcohortfromfile [cohortname] [filename]'
			return
		if TeacherWaitlist.objects.filter(cohort = cohortName).exists():
			print 'cohort already exists!'
			return
		f = open(fileName)
		for line in f.readlines():
			if TeacherWaitlist.objects.filter(email = line.strip()).exists():
				print 'this email already in the database, so we\'ll just update it.'
				for item in TeacherWaitlist.objects.filter(email = line.strip()):
					if item.cohort == "":
						item.cohort = cohortName
					elif item.cohort == cohortName:
						print 'already in this cohort, doing nothing (continue)'
						continue
					else:
						print 'this email was already in another cohort ' + item.cohort + ', replacing it with ' + cohortName
						item.cohort = cohortName
					item.save()
			else:
				newentry = TeacherWaitlist(
					school="skol uf herd noks",
					how_hear="",
					firstname="Charlie",
					lastname="Testnanigans",
					study=True,
					num_students=20,
					email=line.strip(),
					date=timezone.now(),
					convertedToCohort=True,
					cohort=cohortName,
					num_emails_sent=0)
				newentry.save()	
				print "added "+line.strip()+" to cohort "+cohortName
