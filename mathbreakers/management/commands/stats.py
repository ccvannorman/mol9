from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
from mathbreakers import mbcopy
from mathbreakers.util import *
from django.utils import timezone
from mathbreakers.models import *
from mathbreakers.settings import REMOTEDB
from mathbreakers.queries import *

class Command(BaseCommand):

	args = ''
	help = 'global stats'
	def handle(self, *args, **options):
		print get_num_students_all()
