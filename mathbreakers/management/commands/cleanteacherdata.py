from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
import random
from django.core.mail import send_mail

class Command(BaseCommand):


	args = ''
	help = 'remove duplicates in a smart way.'
	def handle(self, verbose=None, *args, **options):
		l = list(TeacherWaitlist.objects.filter(firstname__contains=' '))
		for item in l:
			if not item.firstname[0].istitle():
				print '    firstname: ' + item.firstname
				item.firstname = item.firstname.title()
				print '    is now: ' +item.firstname
			newname = item.firstname.split(' ')[0]
			if not "Mrs" in newname  and not newname == "J" and not newname == "J." and not newname == "R":
				item.firstname = newname
				print 'removed spaces, firstname isnow ' + item.firstname  		
			else:
				print ' skipped .... ' + item.firstname
			if item.firstname == "":
				item.firstname = "Hello"
			# item.save()
			

#below: removing duplicate email addresses while preserving cohort status
#
#		l = list(TeacherWaitlist.objects.all())
#		teachers = {}
#		for item in l:
#			if item.email in teachers:
#				if item.cohort == "":
#					print 'deleting item: ' + item.email
#					item.delete()
#				else:
#					print 'deleting item that was already in list: ' + item.email
#					if TeacherWaitlist.objects.filter(email=item.email,cohort="").exists():
#						TeacherWaitlist.objects.filter(email=item.email,cohort="").first().delete()
#					else:
#						TeacherWaitlist.objects.filter(email=item.email).first().delete()
#						
#
##				print ' duplicate: ' + item.email + " duplicate cohort: " + item.cohort + " orig cohort: " + str(teachers[item.email]["cohort"]["cohort"])
#			else:
#				# print item.email
#				record = {}
#				record["cohort"] = item.cohort
#				teachers[item.email] = {}
#				teachers[item.email]["cohort"] = record #item.cohort
#			#if item.email in teachers["emails"]:
##				if teachers["emails"][item.email]["cohort"] != "":
##					item.delete() #delete this item from the table, a duplicate was found that had a cohort.
##				else:
##					teachers["emails"][item.email]["cohort"] = item.cohort
##			else:
############				teachers["emails"][item.email]["cohort"] = item.cohort
