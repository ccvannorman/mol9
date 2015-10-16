from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
import uuid
import hashlib

class Command(BaseCommand):
    args = 'Number of codes to make'
    help = 'Creates educents codes in the db'

    def handle(self, num, *args, **options):
        for i in range(int(num)):
            code = hashlib.sha1(str(uuid.uuid1()) + "omg so secure").hexdigest()
            print code
            pr = EducentsCode(code=code)
            pr.save()
