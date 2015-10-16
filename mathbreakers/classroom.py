from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from mathbreakers.util import *
from mathbreakers.session import get_real_username, get_student_playtime_seconds
from mathbreakers.models import *
from mathbreakers.forms import *
from mathbreakers.util import *
from mathbreakers import analytics

def get_visible_name(user):
	if len(user.first_name) == 0:
		return user.username
	else:
		return user.first_name

@classroom_required
def manage(request):
	analytics.track_event("visit_teacher_manage_classroom", request=request)
	handle_class_selection(request)
	classroom, all_classes = get_classroom(request)
	return renderWithNav(request, "teacher/manageclass.html", {"classroom":classroom, "classrooms":all_classes, "addclassform": AddClassroomForm() })

iconlookup = {
	1:"onestar",
	2:"twostar",
	3:"threestar"
}

@classroom_required
def dashboard(request):
	analytics.track_event("visit_teacher_dashboard", request=request)
	handle_class_selection(request)
	classroom, all_classes = get_classroom(request)
	db_groups = LevelGroup.objects.order_by('order')
	groups = []
	students = [uca.user for uca in UserClassroomAssignment.objects.filter(classroom=classroom)]
	states = UserLevelState.objects.filter(user__in=students)[::]

	heatmaps = HeatmapPoint.objects.filter(user__in=students).values_list("level_name", flat=True).distinct().values_list("user__username","level_name")
	user_started_levels = {}
	for un,lvl in heatmaps:
		ar = user_started_levels.get(un, [])
		ar.append(lvl)
		user_started_levels[un] = ar

	for g in db_groups:
		if g.secret and not request.user.is_staff:
			continue
		group_owned = True
		if g.upgrade_required and request.user.profile.upgraded == False:
			group_owned = False

		group = {"name":g.name, "levels":[], "owned":group_owned}
		for l in g.levels.all():
			entries = []
			for s in students:
				state = next((st for st in states if st.user == s and st.level == l), None)
				if state is None:
					entry = {"type":"empty"}
				elif state.stars > 0:
					entry = {"type":"stars", "data":iconlookup[state.stars]}
				else:
					entry = {"type":"empty"}
				if state is not None and state.assigned:
					entry["assigned"] = True
				else:
					entry["assigned"] = False
				if l.name in user_started_levels.get(s.username, []):
					if entry["type"] == "empty":
						entry["type"] = "started"
				entry["student"] = s.username
				entry["student_name"] = get_visible_name(s)
				entry["level"] = l.name
				entries.append(entry)
			group["levels"].append({"short_name":l.short_name, "full_name":l.name, "entries":entries})
		groups.append(group)
	groups.sort(lambda a,b:cmp(b['owned'],a['owned']))

	return renderWithNav(request, "teacher/dashboard.html", {"classroom":classroom, "classrooms":all_classes, "groups":groups, "students":students})


@require_http_methods(['POST'])
@classroom_required
def ajax_remove(request):
	username = request.POST['username']
	try:
		classroom, all_classes = get_classroom(request)
		asn = UserClassroomAssignment.objects.get(classroom=classroom, user__username=username)
		asn.delete()
	except:
		return json_response({"success":False})
	return json_response({"success":True})
	

@require_http_methods(['POST'])
@classroom_required
def ajax_assign(request):
	student_name = request.POST['student']
	level_name = request.POST['level']
	student = User.objects.get(username=student_name)
	level = Level.objects.get(name=level_name)

	user = User.objects.get(username=student)
	if not user_in_my_class(request, user):
		return json_response({"success":False})	 

	analytics.track_event("assigned_level", request=request)

	try:		
		uls = UserLevelState.objects.get(user=student, level=level)
		if uls.completed or uls.stars > 0:
			return json_response({"success":False, "error":"Can't assign to a completed level!"})
		else:
			uls.assigned = True
			uls.save()
			return json_response({"success":True})
	except:
		try:
			uls = UserLevelState.create(student, level_name)
			uls.assigned = True
			uls.save()
			return json_response({"success":True})			
		except:
			return json_response({"success":False, "error":"Failed to create assignment"})


@require_http_methods(['POST'])
@classroom_required
def ajax_unassign(request):
	student = request.POST['student']
	level = request.POST['level']
	try:
		user = User.objects.get(username=student)
		if not user_in_my_class(request, user):
			return json_response({"success":False})	 

		uls = UserLevelState.objects.get(user__username=student, level__name=level)
		uls.assigned = False
		uls.save()
		return json_response({"success":True})	
	except:
		return json_response({"success":False})	


@require_http_methods(['GET'])
@classroom_required
def ajax_getstudents(request):
	user = request.user

	students = []
	classroom, all_classes = get_classroom(request)
	for uca in UserClassroomAssignment.objects.filter(classroom=classroom):
		stud = {}
		name = get_visible_name(uca.user)
		stud["username"] = uca.user.username
		stud["name"] = name
		stud["playtime"] = uca.user.profile.playtime / 60
		students.append(stud)
	return json_response({'result':'success', 'students':students})