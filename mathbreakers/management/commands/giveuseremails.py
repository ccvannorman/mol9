from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
import uuid
import hashlib

class Command(BaseCommand):
    args = ''
    help = 'Sets email for users'

    def handle(self, *args, **options):
    	for u in User.objects.filter(email=None) | User.objects.filter(email=""):
    		if "@" in u.username:
    			u.email = u.username
    			u.save()

