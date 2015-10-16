from django.core.management.base import BaseCommand, CommandError
from mathbreakers import models
import uuid
import hashlib
import json
import datetime
from decimal import Decimal

def csvify(x):
	if isinstance(x, bool) or isinstance(x, int) or isinstance(x, float) or isinstance(x, datetime.datetime) or isinstance(x, Decimal):
		return str(x)
	else:
		return json.dumps(str(x))

class Command(BaseCommand):
    args = 'Model name'
    help = 'Outputs a table as csv'

    def handle(self, modelName, *args, **options):
		modelClass = getattr(models,modelName)
		obj = modelClass.objects.all()[0]
		fields = [x.name for x in obj._meta.fields]
		print ",".join(fields)

		for obj in modelClass.objects.all():
			print ",".join( [csvify(getattr(obj, field)) for field in fields] )
