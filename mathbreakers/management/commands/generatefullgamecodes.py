from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
import uuid
import hashlib
from django.utils import timezone

class Command(BaseCommand):
    args = 'number of codes to generate'
    help = 'Generates game purchased codes'

    def handle(self, num, *args, **options):
		spreadsheet = []
		for i in range(int(num)):
			columns = []
			code = uuid.uuid1().hex
			email = "brett.walter@homeschoolbuyersco-op.org"
			gp = GamePurchaseEmail(email=email, time=timezone.now(), code=code)
			gp.save()
			columns.append(code)
			columns.append("https://mathbreakers.com/HSBC/" + code)
			spreadsheet.append(columns)
		print "\n".join([",".join(c) for c in spreadsheet])
