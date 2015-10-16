from mathbreakers.settings import REMOTEDB
from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
import uuid
import hashlib
from django.utils import timezone
from mathbreakers.util import send_mail_sync

class Command(BaseCommand):
    args = 'number of codes to generate'
    help = 'Generates game purchased codes'

    def handle(self, email, *args, **options):
		code = uuid.uuid1().hex
		gp = GamePurchaseEmail(email=email, time=timezone.now(), code=code)
		gp.save()
		print "generated one code for " + email + "; code: " + code
		if not REMOTEDB:
			print "sending mail to " + email + " with new code"
			send_mail_sync(m,s,"robot@imaginarynumber.co",[email])
		else:
			print "did not send mail because REMOTEDB"
