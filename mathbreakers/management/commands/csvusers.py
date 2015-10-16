from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
import uuid
import hashlib

class Command(BaseCommand):
    args = 'Filename with user,password\nuser,password'
    help = 'Creates users from a csv file'

    def handle(self, filename, *args, **options):
		f = open(filename)
		for line in f.readlines():
			username, password = line.strip().split(",")
			u = User.objects.create_user(username, "", password)
			print u
		f.close()
