from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
import uuid
import hashlib

class Command(BaseCommand):
    args = 'Filename with user,password\nuser,password'
    help = 'Creates users from a csv file'

    def handle(self, *args, **options):
    	for u in User.objects.filter(first_name=""):
    		u.first_name = u.username
    		u.save()
