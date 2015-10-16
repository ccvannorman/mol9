from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time 
import datetime
from django.utils import timezone

class Command(BaseCommand):
	args = 'None'
	help = 'imports teacher data from csv'	
	def handle(self, *args, **options):
		day = "2015-04-09"
		date = time.strptime(str(day), "%Y-%m-%d")
		print "date: " +str(date)
		#mt = datetime.fromtimestamp(mktime(struct))
		mt = datetime.datetime(*date[:6])
		print "date2:" +str(mt)
		# nicedate = time.strftime("%A, %B %d",time.gmtime(mt)) #time.gmtime(date))
		# subject = TEACHER_SCHEDULED_A_PLAY_SESSION[0]
		# message = TEACHER_SCHEDULED_A_PLAY_SESSION[1].format("nicedate")
		
