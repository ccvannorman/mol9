from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
import uuid
import hashlib

class Command(BaseCommand):
    args = 'username'
    help = 'Creates a user profile if not exists'

    def handle(self, username, *args, **options):
	u = User.objects.get(username=username)
       	u.is_superuser = True
	u.is_staff = True
	u.save()
	profile, created = UserProfile.objects.get_or_create(user=u)
		
