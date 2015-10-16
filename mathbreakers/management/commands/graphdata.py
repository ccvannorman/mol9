from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from django.db.models import Max, Min, Sum
import datetime, time

class Command(BaseCommand):
    args = 'either "users" or "teachers", number of days per pt'
    help = 'none'

    def handle(self, model, days, *args, **options):
		dates = []
		if model == "users":
			datename = "date_joined"
			modeltype = User
		elif model == "teachers":
			datename = "date"
			modeltype = ClassroomTeacherRel
		elif model == "activity":
			datename = "date"
			modeltype = ClassroomActivityBin
		elif model == "heatmap":
			datename = "time"
			modeltype = HeatmapPoint

		start = modeltype.objects.all().aggregate(Min(datename))[datename+'__min']
		end = modeltype.objects.all().aggregate(Max(datename))[datename+'__max']
		start_seconds = int(time.mktime(start.timetuple()))
		end_seconds = int(time.mktime(end.timetuple()))
		day_seconds = int(days) * 86400
		for cur in range(start_seconds, end_seconds, day_seconds):
			cur -= 86400
			sub_start = datetime.datetime.fromtimestamp(cur)
			sub_end = datetime.datetime.fromtimestamp(cur+day_seconds)
			if model == "users":
				dates.append((cur, User.objects.filter(date_joined__gte=sub_start, date_joined__lt=sub_end).exclude(username__icontains="test").count()))
			elif model == "teachers":
				dates.append((cur, ClassroomTeacherRel.objects.filter(date__gte=sub_start, date__lt=sub_end).count()))
			elif model == "activity":
				activity = ClassroomActivityBin.objects.filter(date__gte=sub_start, date__lt=sub_end).aggregate(Sum("num_seconds"))["num_seconds__sum"]
				if activity == None:
					activity = 0
				dates.append((cur, activity))
			elif model == "heatmap":
				dates.append((cur, HeatmapPoint.objects.filter(time__gte=sub_start, time__lt=sub_end).count()))

		print "\n".join(str(d[0]) + ", " + str(d[1]) for d in dates)
