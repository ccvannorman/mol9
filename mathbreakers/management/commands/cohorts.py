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
		teachers = get_all_teachers_classrooms()
		for item in TeacherWaitlist.objects.all():
			if not item.cohort in cohortList:
				cohortList[item.cohort] = {}
				cohortList[item.cohort]["num_teachers"] = 0
				cohortList[item.cohort]["num_teachers_with_classrooms"] = 0
				cohortList[item.cohort]["num_teachers_with_students"] = 0
				cohortList[item.cohort]["num_teachers_with_licenses"] = 0
				cohortList[item.cohort]["num_total_students"] = 0
				cohortList[item.cohort]["num_total_licenses"] = 0
				cohortList[item.cohort]["num_teachers_no_classrooms"] = 0
				
			else:
				cohortList[item.cohort]["num_teachers"] += 1

			if ClassroomTeacherRel.objects.filter(user__username = item.email).exists():
				if ClassroomTeacherRel.objects.filter(user__username = item.email).first().user.profile.num_licenses > 0:
					cohortList[item.cohort]["num_teachers_with_licenses"] += 1
					cohortList[item.cohort]["num_total_licenses"] += ClassroomTeacherRel.objects.filter(user__username = item.email).first().user.profile.num_licenses 	
				for t in teachers: #hella clumsy and slow
					if t["user"].email == item.email:
						cohortList[item.cohort]["num_total_students"] += t["total_students"]
						if t["total_students"] > 0:
							cohortList[item.cohort]["num_teachers_with_students"] += 1
				cohortList[item.cohort]["num_teachers_with_classrooms"] += 1 
			else:
				cohortList[item.cohort]["num_teachers_no_classrooms"] += 1
		for item in cohortList:
			print str(item)
			print "total teachers in cohort: " + str(cohortList[item]["num_teachers"])
			print "num teachers with classrooms: " + str(cohortList[item]["num_teachers_with_classrooms"])
			print "num teachers with licenses: " + str(cohortList[item]["num_teachers_with_licenses"])
			print "num total licenses: " + str(cohortList[item]["num_total_licenses"])
			print "num total students: " + str(cohortList[item]["num_total_students"])
			
		#print "total licesnes: " + str(totalLicenses) + " / converted: " + str(totalConverted) + " out of " + str(totalTeachers) + ", total not in cohort yet :" + str(totalNotIncohort)

