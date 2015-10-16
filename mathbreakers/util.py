import json
import threading
import datetime
import uuid
import traceback
import time
import random
import urllib

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.middleware import csrf
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from mathbreakers.forms import *
from mathbreakers.mbcopy import *
from mathbreakers.models import *

def handle_class_selection(request):
	if request.GET.has_key("class_selection"):
		request.session['classroom_id'] = request.GET['class_selection']

def classroom_log(classroom, message):
	ClassroomLog(classroom=classroom, message=message, date=timezone.now()).save()

def get_log_str(request, text):
	out = unicode(timezone.now()) + " "
	if request.user.is_anonymous():
		out += "(anon)\n"
	else:
		out += "(" + request.user.username + ")\n"
	out += text
	out += "\n\n"
	return out

def log(request, text):
	print get_log_str(request, text)

def log_error(request):
	text = traceback.format_exc()
	fulltext = get_log_str(request, text)
	log_and_email(request, fulltext)

def log_and_email(request, text):
	print text
	send_mail_threaded(text[0:140], text, "robot@imaginarynumber.co", ["morganquirk@gmail.com"])


def get_ip(request):
	ip = ""
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def classroom_required(view):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated():
			if ClassroomTeacherRel.objects.filter(user=request.user).exists():
				return view(request, *args, **kwargs)	
			else:
				return renderWithNav(request, 'noteacheraccount.html')
		return renderWithNav(request, "nologin.html")
	return wrapper

def get_classroom(request):
	if not request.user.is_authenticated():
		log_and_email(request, "No user, but call to get_classroom!")
		return (None, [])
	classes = ClassroomTeacherRel.objects.filter(user=request.user)
	if classes.count() == 0:
		log_and_email(request, "No classrooms, but call to get_classroom!")
		return (None, [])
	classroom_id = request.session.get('classroom_id', None)
	# If we have the name from our session, use that to get the classroom
	if classroom_id is not None:
		try:
			return (classes.get(classroom__id=classroom_id).classroom, [c.classroom for c in classes])
		except ClassroomTeacherRel.DoesNotExist:
			log_error(request)
	# Otherwise use the first classroom
	return (classes[0].classroom, [c.classroom for c in classes])	

def client_post(view):
	return csrf_exempt(require_http_methods(['POST'])(view))

def client_get(view):
	return csrf_exempt(require_http_methods(['GET'])(view))

def get_or_create_csrf_token(request):
    token = request.META.get('CSRF_COOKIE', None)
    if token is None:
        token = csrf._get_new_csrf_key()
        request.META['CSRF_COOKIE'] = token
    request.META['CSRF_COOKIE_USED'] = True
    return token

def json_response(obj):
	return HttpResponse(json.dumps(obj), content_type="application/json")

def renderWithNav(request, template, obj = None):
	if obj is None:
		obj = {}	
	signin_form = SignInForm()
	if "error" in request.GET:
		obj["error"] = request.GET['error']
	obj["signin_form"] = signin_form
	obj['have_upgrade'] = False
	if request.user.is_anonymous():
		obj["has_class"] = False
		obj["in_class"] = False
	else:
		if request.user.profile.upgraded:
			obj['upgraded'] = True
		else:
			obj['upgraded'] = False
		if True:
			obj['have_upgrade'] = True
		obj['has_class'] = ClassroomTeacherRel.objects.filter(user=request.user).exists()
		obj['in_class'] = UserClassroomAssignment.objects.filter(user=request.user).exists()

	obj['in_session'] = False
	cid=request.session.get('classroom_id', 0)
	an_hour_ago = timezone.now() - datetime.timedelta(hours=1)
	try:
		classroom = Classroom.objects.get(id=cid)
		cs = ClassroomSession.objects.get(classroom=classroom, start_time__gt=an_hour_ago)
		obj['in_session'] = True
	except Classroom.DoesNotExist:
		pass
	except ClassroomSession.DoesNotExist:
		pass

	obj["purchases"] = json.dumps(get_purchases())
	obj["csrf"] = get_or_create_csrf_token(request)
	obj["stripekey"] = ("pk_live_AgMGSLJQPxGOPseElAllUs7w","pk_test_CrGpCg59xvXIuJzacBkgnS8O")[settings.DEBUG]
	obj["buydebug"] = ("false","true")[settings.BUYDEBUG]

	tracking_code = request.COOKIES.get("mb_tracking", None)
	if tracking_code is None:
		tracking_code = uuid.uuid1().hex
	try:
		ct = CohortTracking.objects.get(tracking_cookie=tracking_code)
		obj["cohort"] = ct.cohort
	except:
		cohort = random.choice(["A","B"])
		obj["cohort"] = cohort
		ct = CohortTracking(tracking_cookie=tracking_code, cohort=cohort)
		ct.save()
	response = render(request, template, obj)

	if not request.COOKIES.has_key("mb_tracking"):
		response.set_cookie("mb_tracking", tracking_code,
			expires=365 * 24 * 60 * 60,
			domain=settings.SESSION_COOKIE_DOMAIN,
			secure=settings.SESSION_COOKIE_SECURE or None)

	return response

def mbredirect(path):
	return HttpResponseRedirect(path.replace(" ", "+"))

def make_redirect(path):
	return lambda x:mbredirect(path)

def get_purchases():
	purchases = {}
	for p in PurchaseData.objects.all():
		purchase = model_to_dict(p)
		purchase['price'] = float(purchase['price'])
		purchases[p.code] = purchase
	return purchases

def user_in_my_class(request, student):
	try:
		for ct in ClassroomTeacherRel.objects.filter(user=request.user):
			if UserClassroomAssignment.objects.filter(classroom=ct.classroom, user=student).exists():
				return True
		return False
	except:
		log_error(request)
		return False

class EmailThread(threading.Thread):
	def __init__(self, subject, body, from_email, recipients):
		self.subject = subject
		self.body = body
		self.from_email = from_email
		self.recipients = recipients
		threading.Thread.__init__(self)

	def run(self):
		if 'smtp' in settings.EMAIL_BACKEND:
			time.sleep(random.randint(0, 60))
		try:
			send_mail(self.subject, self.body, self.from_email, self.recipients)
		except Exception as e:
			print str(timezone.now()) + " : Email sending failed to " + str(self.recipients)
			print e

def send_mail_threaded(subject, body, fr, to):
	rse = RobotSentEmail(email=to[0], title=subject, content=body, time=timezone.now())
	rse.save()
	EmailThread(subject, body, fr, to).start()

def send_mail_sync(subject, body, fr, to, dryrun=False):
	if dryrun:
		print '[dryrun] emailed: ' + str(to) + '; subj: ' + subject
		return
	if "morganquirk+" in str(to):
		print ' skipping email to: ' + str(to)
		return
	rse = RobotSentEmail(email=to[0], title=subject, content=body, time=timezone.now())
	rse.save()
	body += """

	
To unsubscribe, click here:
https://mathbreakers.com/unsubscribe/?""" + urllib.urlencode({ "email" : to[0] })
	print 'emailed: ' + str(to) +'; subj: ' + subject
	if Unsubscribed.objects.filter(email=to[0]).exists():
		print "[UNSUBSCRIBED] : " + to[0]
		return
	elif to[0] == "":
		print "[MISSING EMAIL, SKIPPING]"
	else:
		send_mail(subject, body, fr, to)

def tracking_cookie(request):
	try:
		return request.COOKIES["mb_tracking"]
	except:
		return None

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])
