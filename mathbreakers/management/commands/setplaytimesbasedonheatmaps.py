from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table

class Command(BaseCommand):
    args = 'None'
    help = 'Sets play times for users based on their heatmap points'

    def handle(self, *args, **options):
		for u in User.objects.all():
			pts = HeatmapPoint.objects.filter(user=u)
			if pts.exists():
				prof = u.profile
				prof.playtime = pts.count()
				prof.save()
				print u.username + " " + str(pts.count())
