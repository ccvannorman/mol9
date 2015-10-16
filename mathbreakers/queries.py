from django.db.models import Count, Sum, Max

from mathbreakers.models import *


def dupe_count(query, agg_col, out_name="count"):
	return query.values(agg_col).annotate(**{out_name:Count(agg_col)}).values_list(agg_col, out_name)

def dupe_sum(query, agg_col, sum_col, out_name="sum"):
	return query.values(agg_col).order_by(agg_col).annotate(**{out_name:Sum(sum_col)}).values_list(agg_col,out_name)

def dupe_max(query, agg_col, max_col, out_name="max"):
	return query.values(agg_col).order_by(agg_col).annotate(**{out_name:Max(max_col)}).values_list(agg_col,out_name)

def dupe_count_as_dict(query, agg_col):
	lst = dupe_count(query, agg_col)
	return {k:v for k,v in lst}

def dupe_sum_as_dict(query, agg_col, sum_col):
	lst = dupe_sum(query, agg_col, sum_col)
	return {k:v for k,v in lst}

def dupe_max_as_dict(query, agg_col, max_col):
	lst = dupe_max(query, agg_col, max_col)
	return {k:v for k,v in lst}

def get_all_teachers_classrooms():
	"""
	Returns all teachers and their classrooms in a big list. Each entry of the list looks like
	{
		"user": <user object>,
		"classrooms":[<classroom object>, ...],
		"total_playtime": <num> (minutes),
		"total_students": <num>,
		"date_joined": <datetime>,
	}
	Each classroom object has the classroom model fields plus three extra fields:
	classroom.playtime - total number of ,inutes played
	classroom.num_students - number of students in the class
	user.date_joined - the date the teacher signed up
	"""
	student_count = dupe_count_as_dict(UserClassroomAssignment.objects, "classroom")
	playtime = dupe_sum_as_dict(ClassroomActivityBin.objects, "classroom", "num_seconds")	
	latest = dupe_max_as_dict(ClassroomActivityBin.objects, "classroom", "date")

	teachers = {}
	for ctr in ClassroomTeacherRel.objects.all():
		u = ctr.user
		cls_playtime = playtime.get(ctr.classroom.id, 0) / 60.0
		cls_students = student_count.get(ctr.classroom.id, 0)

		obj = teachers.get(u, {})
		obj["user"] = u

		obj["latest_activity"] = latest.get(ctr.classroom.id, 0)

		classrooms = obj.get("classrooms", [])
		ctr.classroom.playtime = cls_playtime
		ctr.classroom.num_students = cls_students
		classrooms.append(ctr.classroom)
		obj["classrooms"] = classrooms

		total_playtime = obj.get("total_playtime", 0)
		total_playtime += cls_playtime
		obj["total_playtime"] = total_playtime

		total_students = obj.get("total_students", 0)
		total_students += cls_students
		obj["total_students"] = total_students		

		obj["date_joined"] = u.date_joined

		teachers[u] = obj
	return teachers.values()

def get_num_teacher_students(user):
	return user.classroomteacherrel_set.aggregate(\
		total = Count("classroom__userclassroomassignment"))["total"]

def get_student_playtime_seconds(user):
	seconds = user.classroomteacherrel_set.aggregate(\
		total = Sum("classroom__classroomactivitybin__num_seconds"))["total"]
	if seconds is None:
		return 0
	else:
		return seconds

def get_playtime_limit_seconds(user):
	return get_num_teacher_students(user) * 3600

def is_trial_half_expired(user):
	limit = get_playtime_limit_seconds(user)
	if limit > 0:
		return get_student_playtime_seconds(user) >= limit / 2
	else:
		return False

def is_trial_expired(user):
	limit = get_playtime_limit_seconds(user)
	if limit > 0:
		return get_student_playtime_seconds(user) >= limit
	else:
		return False

def get_num_students_all():
	teachers = get_all_teachers_classrooms()
	num_students = 0
	for teacher in teachers:
		num_students += teacher["total_students"]
	return num_students

def get_teachers_total_licenses():
	return UserProfile.objects.filter(num_licenses__lt=999,num_licenses__gt=0).aggregate(Sum("num_licenses"))

def get_teachers_total_who_have_playtime():
	teachers = get_all_teachers_classrooms()
	total = 0
	for t in teachers:
		if t["total_playtime"] > 10:
			total += 1
	return total

def get_all_students_playtime():
	teachers = get_all_teachers_classrooms()
	total = 0
	for t in teachers:
		total += t["total_playtime"]
	return total

def get_teachers_with_paid_classrooms():
	teachers = get_all_teachers_classrooms()
	total = 0
	for t in teachers:
		if t["user"].profile.num_licenses > 0:
			total += 1
	return total
	
def get_total_home_purchases():
	PurchaseRecord.objects.filter(code="mbfull").count()
