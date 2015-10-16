from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
import random
from django.core.mail import send_mail
from mathbreakers.util import *
class Command(BaseCommand):

	args = ''
	help = 'emails the appropriate trickle to some databased peoples'
    	def handle(self, subject="defaultsubject", message="defaultmessage", email="charlie@imaginarynumber.co", *args, **options):
		send_mail_threaded(subject, message, "from_mathbreakers@mathbreakers.com", [email])
