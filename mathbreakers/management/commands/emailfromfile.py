from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
from mathbreakers import mbcopy

from mathbreakers.util import *
from django.utils import timezone
import os.path

class Command(BaseCommand):

	args = ''
	help = 'emails the appropriate trickle to some databased peoples'
    	def handle(self, emailfile=None, emailNo=0, whichAB="none", ABTestDescription="none", dryrun="", *args, **options):
		dryrun = dryrun == "dryrun"
		print "dryrun:" + str(dryrun)
		if emailfile is None or emailNo == 0 or whichAB  == "none" or ABTestDescription == "none":
			print 'usage: [emailfile.txt]  [email # 1, 2, 3..]  [ABtest "testA","testB"],  [ABTest description]'
			return
		emailNo = int(emailNo)		

		ABTestUrl = ""
		if whichAB == "testA":
			ABTestUrl = "mathbreakers.com/start/A"
		elif whichAB == "testB":
			ABTestUrl = "mathbreakers.com/start/B"
		else:
			print "not a valid test: "+whichAB
			print "exiting --"
			return

		message = ""
		subject = "" 
		f = open(emailfile)
		numsent = int(0)
		for line in f:
			line = line.strip()
			if emailNo == 1:
				subject = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_1[0].format("Hey")
				message = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_1[1].format("Hello",ABTestUrl)
			elif emailNo == 2:
				subject = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_2[0].format("Hey")
				message = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_2[1].format("Hello",ABTestUrl)
			elif emailNo == 3:
				subject = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_3[0].format()
				message = mbcopy.TEACHER_TRICKLE_EMAIL_NO_CLASSROOM_YET_3[1].format("Hello",ABTestUrl)
			else:
				print 'something went wrong and no email was sent'
				return
			send_mail_sync(subject, message, "charlie@mathbreakers.com", [line], dryrun)
			time.sleep( 1 )
			numsent += 1
			print 'sent a message to ' + line	
			
		sub = "Just sent "+str(numsent)+" emails of type "+str(emailNo)+" to teachers in file "+emailfile
		if dryrun:
			sub = "[dryrun]: " + sub
		mes = """the last email sent was ..:
			subject:""" + subject + """
			""" + "body:" + message[:40] + "...." 
		print 'no database records were updated.'
		print ""
		print ""

		send_mail(sub,mes,"robot@mathbreakers.com",["team@mathbreakers.com"])
		


