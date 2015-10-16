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
	def handle(self, cohortName=None, cohortQuantity=None, big=False, *args, **options):
		if cohortName is None or cohortQuantity is None:
			print 'usage: newcohort [name] [qty] [big]'
			return
		if TeacherWaitlist.objects.filter(cohort = cohortName).exists():
			print 'cohort already exists!'
			return
		big = big == "big"
		if big == False:
			filteredList = list(TeacherWaitlist.objects.filter(num_students__lt=250,cohort=""))
		else:
			filteredList = list(TeacherWaitlist.objects.filter(num_students__gt=249,cohort=""))
			
		random.shuffle(filteredList)
		emails = []
		for item in filteredList[0:int(cohortQuantity)]:
			item.cohort = cohortName
			item.convertedToCohort=True
			item.save()
			emails.append(item.email)
		print ','.join(emails)

