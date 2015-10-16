from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
import uuid
import hashlib

class Command(BaseCommand):
    args = 'ip address'
    help = 'Deletes classrooms and sessions associated with an ip address'

    def handle(self, ip, *args, **options):
		sessions = ClassroomSession.objects.filter(ip=ip)
		for c in sessions:
			print "Session: " + str(c)
			print "Classroom: " + str(c.classroom)
		yn = raw_input("Delete these? y/n>")
		if yn.strip() != "y":
			return
		print "Deleting"
		for c in sessions: 
			c.classroom.delete()
			c.delete()
