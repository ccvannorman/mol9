from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table

class Command(BaseCommand):
    args = 'filename of py dict'
    help = 'Moves users from old level names to new level names'

    def handle(self, mappingfile, *args, **options):
		f = open(mappingfile,"r")
		mapping = eval(f.read())
		f.close()

		for oldn, newn in mapping.items():
			ulss = UserLevelState.objects.filter(level__name=oldn)
			print oldn + " -> " + newn + " (" + str(ulss.count()) + " items)"
			try:
				newl = Level.objects.get(name=newn)
			except Level.DoesNotExist:
				newl = Level(name=newn, short_name=newn[:10])
				newl.save()
			for uls in ulss:
				if not UserLevelState.objects.filter(level=newl).exists():
					uls.level = newl
					uls.save()