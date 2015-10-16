import datetime
import time
import hashlib
import uuid
import random

from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse

import pytz

from mathbreakers.util import *
from mathbreakers.models import *
from mathbreakers.auth import *
from mathbreakers.mbcopy import *
from mathbreakers.forms import *
from mathbreakers.queries import *


def su_required(view):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated() and request.user.is_superuser:
			return view(request, *args, **kwargs)
		return renderWithNav(request, "404.html")
	return wrapper

@su_required
def buttons(request, sincestamp):
	ips = {}
	stats = {}
	since = datetime.datetime.fromtimestamp(float(sincestamp))
	times = [0, time.time() - 60*60*24, time.time() - 60*60*24*7]
	for btn in ButtonLog.objects.filter(time__gte=since):
		name = btn.page + ":" + btn.name
		entry = stats.get(name, 0)
		stats[name] = entry + 1

		ipname = btn.ip
		if btn.user:
			ipname += " -- " + btn.user.username
		lob = ips.get(ipname, list())
		lob.append(btn.page+ ":" + btn.name)
		ips[ipname] = lob

	ordered_stats = [(k,v) for k,v in stats.items()]
	ordered_stats.sort(lambda a,b:cmp(b[1],a[1]))

	uniques = []
	for ip, btns in ips.items():
		total = len(btns)
		different = len(set(btns))
		uniques.append((ip, total, different))
	uniques.sort(lambda a,b:cmp(a[0],b[0]))
		
	return renderWithNav(request, "su/buttons.html", {"stats":ordered_stats, "uniques":uniques, "times":times, "since":sincestamp})

@su_required
def buttons_for(request, sincestamp, ipname):
	since = datetime.datetime.fromtimestamp(float(sincestamp))
	clicks = []
	ip = ipname
	btns = None
	try:
		ip, name = ipname.split(" -- ")
		btns = ButtonLog.objects.filter(ip=ip,user__username=name, time__gte=since)
	except:
		ip = ipname
		btns = ButtonLog.objects.filter(ip=ip, user=None, time__gte=since)
	for btn in btns:
		clicks.append((btn.time.ctime(), btn.page + ":" + btn.name))

	clicks.sort(lambda a,b:cmp(a[0],b[0]))

	return renderWithNav(request, "su/buttons_for.html", {"stats":clicks})

@su_required
def campsignups(request):
	signups = [cs for cs in CampSignup.objects.filter(paid=True)]
	signups.sort(lambda a,b:cmp(a.session,b.session))
	return renderWithNav(request, "su/campsignups.html", {"signups":signups})


@su_required
def purchase_users(request):
	gp = []
	for p in GamePurchase.objects.all():
		delta = p.time - p.user.date_joined
		gp.append(p.user.username + ": " + str(delta))
	return renderWithNav(request, "su/list.html", {"title":"Users who have purchesd", "list":gp})

@su_required
def user_progress(request):
	num_levels = {}
	for st in UserLevelState.objects.all():
		if st.completed:
			if num_levels.has_key(st.user):
				num_levels[st.user][0] += 1
			else:
				num_levels[st.user] = [1,0]
		if st.assigned:
			if num_levels.has_key(st.user):
				num_levels[st.user][1] += 1
			else:
				num_levels[st.user] = [0,1]

	for user in User.objects.all():
		if not num_levels.has_key(user):
			num_levels[user] = [0,0]

	user_levels = [(k, v) for k,v in num_levels.items()]
	user_levels.sort(lambda a,b:cmp(b[1][0] + b[1][1], a[1][0] + a[1][1]))
	return renderWithNav(request, "su/userprogress.html", {"user_levels":user_levels})

@su_required
def preorder(request):
	code = hashlib.sha1(str(uuid.uuid1()) + "omg so secure").hexdigest()
	pr = PreorderRegistration(code=code, user=None)
	pr.save()
	return renderWithNav(request, "su/preorder.html", {"code":pr.code})

@su_required
def generatefullgamecode(request):
	code = uuid.uuid1().hex
	if request.method=='POST':
		email = request.POST["email"]
	else:
		email = request.GET['email']
	gp = GamePurchaseEmail(email=email, time=timezone.now(), code=code)
	gp.save()
	s = "Your Mathbreakers full game code"
	m = """Hello!

Here is your full game code from Mathbreakers. Please follow this link and download the game from our website.

{0}

Happy Mathbreaking!

-The team
	"""
	send_mail_threaded(s,m.format("https://mathbreakers.com/download/full/"+gp.code+"/"),"robot@imaginarynumber.co",[email])
	return renderWithNav(request, "su/generatefullgamecode.html",{"code":gp.code,"email":gp.email,"success":True})


@su_required
def classrooms(request):
	classes = []
	trial_period = datetime.timedelta(days=31)
	for ctr in ClassroomTeacherRel.objects.all():
		info = {}
		info['name'] = ctr.classroom.name
		info['email'] = ctr.user.email
		info['username'] = ctr.user.username
		info['firstname'] = ctr.user.first_name
		info['lastname'] = ctr.user.last_name
		info['school'] = ctr.classroom.school 
		info['students'] = []
		for cua in UserClassroomAssignment.objects.filter(classroom=ctr.classroom):
			info['students'].append(cua.user.username)	
		info['numstudents'] = len(info['students'])
		remaining = (ctr.date + trial_period) - timezone.now()
		week_ago = timezone.now() - datetime.timedelta(days=7)
		month_ago = timezone.now() - datetime.timedelta(days=31)
		info['weeklyactivity'] = sum([cab.num_seconds / 60.0 for cab in
			ClassroomActivityBin.objects.filter(classroom=ctr.classroom, date__gt=week_ago)])
		info['monthlyactivity'] = sum([cab.num_seconds / 60.0 for cab in
			ClassroomActivityBin.objects.filter(classroom=ctr.classroom, date__gt=month_ago)])
		info['totalactivity'] = sum([cab.num_seconds / 60.0 for cab in
			ClassroomActivityBin.objects.filter(classroom=ctr.classroom)])

		info['trialdays'] = remaining.days

		classes.append(info)
	secondsort = request.GET.get("secondsort", "weeklyactivity")
	if secondsort[0] == "-":
		secondsort = secondsort[1:]
		classes.sort(lambda a,b:cmp(b[secondsort], a[secondsort]))
	else:
		classes.sort(lambda a,b:cmp(a[secondsort], b[secondsort]))


	sort = request.GET.get("sort", "totalactivity")
	if sort[0] == "-":
		sort = sort[1:]
		classes.sort(lambda a,b:cmp(b[sort], a[sort]))
	else:
		classes.sort(lambda a,b:cmp(a[sort], b[sort]))
	return renderWithNav(request, "su/classrooms.html", {"classes":classes})

@su_required
def index(request):
	return renderWithNav(request, "su/su.html")

hug_texts = [
"u1r7beautiful",
"robot3love2u",
"hug8hug",
"click5me",
"robot65heart",
]

def make_a_hug(email, referral):
	code = "hug" + str(VirtualHug.objects.count() + 1)
	vh = VirtualHug(code=code, email=email, referral=referral)
	vh.save()
	return code

@su_required
def makehugs(request):
	if request.method=='POST':
		for email in [x.strip() for x in request.POST['emaillist'].split(",")]:
			if len(email) < 4:
				continue
			if VirtualHug.objects.filter(email=email).exists():
				continue
			code = make_a_hug(email, False)
			send_mail(HUG_EMAIL[0], HUG_EMAIL[1] % (code,), "robot@imaginarynumber.co", [email])
		return HttpResponseRedirect("/su/")
	else:
		return renderWithNav(request, "su/makehugs.html")

@su_required
def getsurveys(request):
	surveys = EmailSurvey.objects.all()
	return renderWithNav(request, "su/survey.html", {"surveys":surveys})

@su_required
def recent_classroom_activity(request):
	pass

@su_required
def ajax_mark_teacher(request):
	tracking = request.POST["tracking"]
	column = request.POST["column"]
	value = request.POST["value"] == "true"
	print tracking, column, value
	try:
		note = SUTeacherNote.objects.get(tracking_cookie=tracking, column=column)
		note.checked=value		
	except SUTeacherNote.DoesNotExist:
		note = SUTeacherNote(tracking_cookie=tracking, column=column, checked=value)
	note.save()
	return json_response({"success":True})

cohort_colors = [
"#d85c40",
"#7789e7",
"#ffe071",
"#c369dd",
"#96df79",
"#e5637e",
"#5fd0b4",
"#cccccc",
"#657288",
]


#@su_required
def partnerships(request):
	partnerships = list(Partnerships.objects.all())
	return renderWithNav(request, "su/partnerships.html", {"partnerships":partnerships})



@su_required
def teacher_signup_flow(request):
	sortby = request.GET.get('sort', None)

	objs = list(TeacherSignupFlow.objects.all())

	cohorts_list = request.GET.get('cohorts', '')
	all_cohorts = enumerate(list(set([o.cohort for o in objs if o.cohort is not None])))
	if len(cohorts_list.strip()) == 0:
		cohorts = all_cohorts
	else:
		cohorts = enumerate([cn.strip() for cn in cohorts_list.split(",")])
	cohorts_dict = {l[1]:l[0] for l in cohorts}

	tdict = {}
	for t in objs:
		tdict[t.tracking_cookie] = t
		if t.cohort in cohorts_dict:
			t.cohort_color = cohort_colors[cohorts_dict[t.cohort]]
		else:
			t.cohort_color = "#ffffff"
	
	for note in SUTeacherNote.objects.all():
		try:
			setattr(tdict[note.tracking_cookie], "note_"+note.column, note.checked)
		except:
			print note.tracking_cookie

	teachers = list(tdict.values())
	

	def sortnote(colname):
		def srt(x,y):
			xn = getattr(x, "note_"+colname, False)
			yn = getattr(y, "note_"+colname, False)
			return cmp(xn,yn)
		return srt

	sortfns = {
		"students_joined":lambda x,y:cmp(x.num_students, y.num_students),
		"student_playtime":lambda x,y:cmp(x.playtime, y.playtime),
		"paid":lambda x,y:cmp(x.purchase_price, y.purchase_price),
		"max_level":lambda x,y:cmp(x.max_level_reached, y.max_level_reached),
		"check_A":sortnote("a"),
		"check_B":sortnote("b"),
		"check_C":sortnote("c"),
		"email":lambda x,y:cmp(get_flipped_email(x.username),get_flipped_email(y.username)),
	}

	if sortby is not None:
		if sortby[0] == '-':
			teachers.sort(lambda x,y:sortfns[sortby[1:]](y,x))
		else:
			teachers.sort(sortfns[sortby])	

	else:
		teachers.sort(lambda x,y:cmp(y.order,x.order))

	return renderWithNav(request, "su/teacher_signup_flow.html", {"teachers":teachers, "cohortslist":cohorts_list})


@su_required
def userinfo(request):
	links = []
	username = request.GET.get('username', None)
	if username is None:
		return renderWithNav(request, "su/userinfo.html", {"username":username, "links":[]})
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return renderWithNav(request, "su/userinfo.html", {"username":username, "links":[]})
	links.append({
		"name":"User model",
		"url":"/admin/auth/user/" + str(user.id) + "/"
	})
	links.append({
		"name":"Login as " + username,
		"url":"/su/loginas/" + username + "/"
	})
	links.append({
		"name":"User Profile" + ("", " (teacher license)")[user.profile.upgraded],
		"url":"/admin/mathbreakers/userprofile/" + str(user.profile.id) + "/"
	})

	
	for uca in UserClassroomAssignment.objects.filter(user=user):
		links.append({
			"name":"Student of classroom: " + uca.classroom.name,
			"url":"/admin/mathbreakers/classroom/" + str(uca.classroom.id) + "/"
		})
		teacher = ClassroomTeacherRel.objects.get(classroom=uca.classroom).user
		links.append({
			"name":" - Teacher: " + teacher.username,
			"url":"/su/userinfo?username=" + teacher.username
		})		


	for ctr in ClassroomTeacherRel.objects.filter(user=user):
		extra = ""
		links.append({
			"name":"Teacher of classroom: " + ctr.classroom.name + extra,
			"url":"/admin/mathbreakers/classroom/" + str(ctr.classroom.id) + "/"
		})

		for uca in UserClassroomAssignment.objects.filter(classroom=ctr.classroom):
			minutes = uca.user.profile.playtime / 60
			links.append({
				"name":" - Student: " + uca.user.username + " (%d minutes played)" % minutes,
				"url":"/su/userinfo?username=" + uca.user.username
			})

	for uls in UserLevelState.objects.filter(user=user):
		levelstate = "-"
		if uls.assigned:
			levelstate = "assigned"
		if uls.completed:
			levelstate = "completed"
		links.append({
			"name": "+ Level " + uls.level.name + " (%s)" % levelstate,
			"url": "/admin/mathbreakers/userlevelstate/" + str(uls.id) + "/"
		})

	for pr in PurchaseRecord.objects.filter(user=user):
		links.append({
			"name": "Purchase: " + pr.code + " for $%0.2f" % float(pr.price / 100.0),
			"url": "/admin/mathbreakers/purchaserecord/" + str(pr.id) + "/"
		})

	buttons = " > ".join([bl.name for bl in ButtonLog.objects.filter(user=user).order_by("time")])

	return renderWithNav(request, "su/userinfo.html", {"username":username, "links":links, "buttons":buttons})

def loginas(request, username):
	user = perform_signin_no_password(request, username)
	response = HttpResponseRedirect("/")
	response.set_cookie("fakelogin", True)
	return response

def get_flipped_email(email):
	
	if email is None:
		return "zzz"
	try:
		sp = email.split("@")
		return (sp[1] + "/" + sp[0]).lower()
	except:
		return "/"+email.lower()

def emailsort(x,y):
	ef = get_flipped_email
	return cmp(ef(x['user'].email), ef(y['user'].email))

def latestsort(x,y):
	x = x['latest_activity']
	y = y['latest_activity']
	if x != 0:
		x = time.mktime(x.timetuple())
	if y != 0:
		y = time.mktime(y.timetuple())
	return cmp(x,y)

def datejoinedsort(x,y):
	return cmp(x['user'].date_joined, y['user'].date_joined)


@su_required
def teachers(request):
	sort = request.GET.get("sort", "-tplaytime")
	sort_fns = {
		"tplaytime":lambda x,y:cmp(x["total_playtime"], y["total_playtime"]),
		"tstudents":lambda x,y:cmp(x["total_students"], y["total_students"]),
		"tlatest":latestsort,
		"email":emailsort,
	}
	teachers = get_all_teachers_classrooms()
	
	for t in teachers:
		if t["latest_activity"] != 0 and (timezone.now() - t["latest_activity"]).total_seconds() < 3600:
			t["active"] = True

	try:
		if sort[0] == '-':
			teachers.sort(lambda x,y:sort_fns[sort[1:]](y,x))
		else:
			teachers.sort(sort_fns[sort])
	except:
		pass
	
	return renderWithNav(request, "su/teachers.html", {"teachers":teachers})

@su_required
def company_stats(request):
	data = {}
	data["total_licenses"] = get_teachers_total_licenses()
	data["num_teachers_contacted"] = TeacherWaitlist.objects.count()
	data["num_teachers_with_classrooms"] = len(get_all_teachers_classrooms())
	data["num_paid_classrooms"] = get_teachers_with_paid_classrooms()
	data["num_total_licenses"] = get_teachers_total_licenses()
	data["num_teachers_with_playtime"] = get_teachers_total_who_have_playtime() 
	data["num_students_in_classrooms"] = get_num_students_all() 
	data["total_playtime"] = get_all_students_playtime()
	data["total_home_purchases"] = GamePurchaseEmail.objects.filter(downloads__gt=0).count() + 50  #explanation for +50 fudge factor: when the game was $5, $10 and $15 preorders, those did not go into purchase datas. We have the paypal and stripe records for these if we REALLY want them. 
	return renderWithNav(request, "su/company_stats.html", {"data":data})


@su_required
def list_teacher_emails(request):
	teachers = get_all_teachers_classrooms()
	sort = request.GET.get("sort","-tdatejoined")
	sort_fns = {
		"tdatejoined":datejoinedsort,
		"email":emailsort,
	}
	try:
		if sort[0] == '-':
			teachers.sort(lambda x,y:sort_fns[sort[1:]](y,x))
		else:
			teachers.sort(sort_fns[sort])
	except:
		pass

	return renderWithNav(request, "su/teacher_emails.html", {"teachers":teachers})

#@su_required
#def manage_school_licenses(request):	
#	if request.method=='POST':
#		email = request.POST["email"]
#	else:
#		email = request.GET['email']
#	teachers = get_all_teachers_classrooms()
#	teachers = teachers.objects.filter(email=email)	
#	
#	return renderWithNav(request, "su/manage_licenses.html", {"teachers":teachers})


