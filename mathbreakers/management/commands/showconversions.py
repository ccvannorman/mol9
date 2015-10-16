from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.util import *
from mathbreakers.commoncore import get_cc_table
import time
import datetime
import random
from django.utils import timezone
from mathbreakers.queries import get_all_teachers_classrooms

class Command(BaseCommand):
	args = 'cohort letter, cohort qty'
	help = 'checks against teacher classrom rel for conversions from teacherwaitlist to lobby sessions'
	def handle(self, *args, **options):
		totalConverted = 0
		totalTeachers = 0
		totalLicenses = 0
		totalNotIncohort = 0
		cohortList = {}
		teachers = get_all_teachers()
		for item in TeacherWaitlist.objects.all():
			if not item.cohort in cohortList:
				cohortList[item.cohort] = {}
				cohortList[item.cohort]["num_teachers"] = 0
				cohortList[item.cohort]["num_conversions"] = 0
				cohortList[item.cohort]["num_licenses"] = 0
				# print ' added cohort: ' + str(cohortList[item.cohort]) + "; " + item.cohort
			else:
				cohortList[item.cohort]["num_teachers"] += 1

			if ClassroomTeacherRel.objects.filter(user__username = item.email).exists():
				cohortList[item.cohort]["num_teachers"] +=1
				cohortList[item.cohort]["num_conversions"] += 1
				cohortList[item.cohort]["num_licenses"] += ClassroomTeacherRel.objects.filter(user__username = item.email).first().user.profile.num_licenses
				# print ' added 1 to cohort: ' + str(cohortList[item.cohort]) + "; " + item.cohort
		for item in cohortList:
			# print "num teachers converted from cohort " + str(item) + " was " + str(item["num_conversions"]) + " out of " + str(item["num_teachers"])
			totalConverted += cohortList[item]["num_conversions"]
			totalTeachers += cohortList[item]["num_teachers"]
			totalLicenses += cohortList[item]["num_licenses"]
		print "total licesnes: " + str(totalLicenses) + " / converted: " + str(totalConverted) + " out of " + str(totalTeachers) + ", total not in cohort yet :" + str(totalNotIncohort)
