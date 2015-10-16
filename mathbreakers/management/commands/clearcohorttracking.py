from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
import random
from django.utils import timezone
from django.core.management import call_command

class Command(BaseCommand):
	args = 'cohort letter, cohort qty'
	help = 'selects 50 teachers and puts them into a cohort'
    	def handle(self, *args, **options):
			CohortTracking.objects.all.delete()
			Django.core.
			
