from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
import random
from django.core.mail import send_mail
import sys
from django.conf import settings
class Command(BaseCommand):

	args = ''
	help = 'clears the teacher table'
    	def handle(self,  *args, **options):
		question = "Really clear the teacher table of all data? This is probably not a good idea if you're on the production server..."
		prompt = " [y/n] "
		choice = "n"
		if not settings.DEBUG:
			print "sorry, you tried this on production server. Returning"
			return
		while True:
			sys.stdout.write(question + prompt)
			choice = raw_input().lower()
			if choice == "y":
				print "ok buddy I hope you know what yer doin"
				TeacherWaitlist.objects.all().delete()
				print "Teacher waitlist table now empty"
				return
			elif choic == "n":
				print "nothing deleted"
				return
			else:
			    sys.stdout.write("Please respond with 'yes' or 'no' "
					     "(or 'y' or 'n').\n")	
		print "your choice was: "+choice
