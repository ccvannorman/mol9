from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
from mathbreakers import mbcopy
from mathbreakers.util import *
from django.utils import timezone
from mathbreakers.session import *
from django.utils import timezone
from mathbreakers.queries import get_all_teachers_classrooms
class Command(BaseCommand):

	args = ''
	help = 'sometimes organics make classes that werent on our waitlist so lets add them to waitlist'
	def handle(self, *args, **options):
		teachers = get_all_teachers_classrooms()
		for to in teachers:
			u = to["user"]
			if not TeacherWaitlist.objects.filter(email=u.email).exists():
				
				print 'email doesnt exist, adding to "teacherwaitlist" table: ' + u.email
				newentry = TeacherWaitlist(school="",
					how_hear="organic",
					firstname="",
					lastname="",
					study=False,
					num_students=to["total_students"],
					email=u.email,
					date=timezone.now(),
					convertedToCohort=False,
					cohort="",
					num_emails_sent=0)
				newentry.save()


