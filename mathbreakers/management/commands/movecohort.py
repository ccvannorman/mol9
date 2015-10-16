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
    	def handle(self, cohortFrom=None, cohortTo=None, *args, **options):
		if cohortFrom is None or cohortTo is None:
			print 'usage: movecohort A B will set all teachers in cohort A to cohort B'
			return
	
		filteredList = list(TeacherWaitlist.objects.filter(cohort=cohortFrom))
		numChanged = 0;
		emailsChanged = "";
		for item in filteredList:
			item.cohort = cohortTo
			item.save()
			numChanged += 1
			emailsChanged += item.email +","
		print "moved " + str(numChanged) + " cohorts from " + cohortFrom + " to " + cohortTo + ", emailschanged was; "+emailsChanged


