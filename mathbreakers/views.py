import json
import uuid
import mbcopy
import urllib
import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.contrib import auth
from django.forms.util import ErrorList

import requests

from mathbreakers import analytics
from mathbreakers.forms import *
from mathbreakers.auth import perform_signin, perform_logout
from mathbreakers.models import *
from mathbreakers.util import *
from mathbreakers.su import make_a_hug
from mathbreakers.ajax import post_data_email_signup
from mathbreakers.session import make_session


def home(request):
	ip = request.META.get('REMOTE_ADDR', None)
	if request.user.is_authenticated():
		bl = ButtonLog(page="home", name="visit", user=request.user, ip=ip, time=timezone.now())
	else:
		bl = ButtonLog(page="home", name="visit", ip=ip, time=timezone.now())
	bl.save()

	analytics.track_event("visit_home", request)

	obj = {}
	obj['bought'] = False
	obj['have_email'] = "false"
	obj['newslettered'] = False

	if request.GET.has_key('yup'):
		obj['newslettered'] = True

	if not request.user.is_anonymous():
		#ew hack
		if request.user.email == "none@none.com" or request.user.email == "":
			obj['have_email'] = "false"
		else:
			obj['have_email'] = "true"
		if GamePurchase.objects.filter(user=request.user).exists():
			obj['bought'] = True
	return renderWithNav(request, 'home.html', obj)

def logout(request):
	perform_logout(request)
	response = HttpResponseRedirect('/')
	response.delete_cookie("mb_tracking")
	response.delete_cookie("fakelogin")
	return response

# Takes a template, returns a view which returns that template. This eliminates
# the need to always create custom functions for one-off simple pages.
def simple_page(template):
	def handler(request):
		event_name = "visit_" + request.path.strip("/").replace("/","_")
		analytics.track_event(event_name, request)
		return renderWithNav(request, template)
	return handler

def notify(request):
	return HttpResponseRedirect('/preorder/')

def presskit(request):
	return renderWithNav(request, 'presskit.html')

def redirect(other):
	def handler(request):
		return HttpResponseRedirect(other)
	return handler

def labs(request):
	experiments = MathExperiment.objects.filter()
	return renderWithNav(request, 'labs.html', {'experiments':experiments})

def message(request):
	return renderWithNav(request, 'message.html', {"title":request.GET['title'], "description":request.GET['description']})

def message_teacher(request):
	return renderWithNav(request, 'message_teacher.html', {"title":request.GET['title'], "description":request.GET['description']})

def trial(request):
	return HttpResponseRedirect("/session/try/")

def forgotpassword(request):
	if request.method == 'POST':
		form = ForgotPasswordForm(request.POST)
		if form.is_valid():
			emailusers = User.objects.filter(email=form.cleaned_data["email"])
			if len(emailusers) > 0:
				emailuser = emailusers[0]
				emailaddr = emailuser.email

				# Build a password reset object so we can have a hash which we send to their email
				code = uuid.uuid1().hex
				pr = PasswordReset(user=emailuser, code=code, time=timezone.now())
				pr.save()

				# Write the email
				subject = "Password reset request for Mathbreakers"
				link = "https://mathbreakers.com/passwordreset/" + code
				message = "Someone clicked the \"I forgot my password\" button for your account. If this was you, reset it here: " + link + "\nIf it wasn't, ignore this!"
				send_mail_threaded(subject, message, "robot@imaginarynumber.co", [emailaddr])

				return mbredirect("/message/?title=Password reset email sent&description=Click the link inside the email to reset the password")
			else:
				form._errors["email"] = ErrorList([u"There's no account associated with that email address."])
				return renderWithNav(request, 'forgotpassword.html', {"form":form})	
			
		else:
			return renderWithNav(request, 'forgotpassword.html', {"form":form})	
	else:
		return renderWithNav(request, 'forgotpassword.html', {"form":ForgotPasswordForm()})

def passwordreset(request, code):
	try:
		pr = PasswordReset.objects.get(code=code)		
		if request.method == 'POST':
			form = PasswordResetForm(request.POST)
			if form.is_valid():
				pr.user.set_password(form.cleaned_data["new_password"])
				pr.user.save()
				pr.delete()				
				return mbredirect("/message/?title=Account password successfully reset&description=You should now be able to log in to the game and website using your new password")
			else:
				return renderWithNav(request,"passwordreset.html", {"form":form, "username":pr.user.username, "code":code})		
		else:
			return renderWithNav(request,"passwordreset.html", {"form":PasswordResetForm(), "username":pr.user.username, "code":code})
	except:
		log_error(request)
		return mbredirect("/message/?title=Bad password reset code&description=Bad password reset code")
		
def download_full(request, code):
	try:
		gp = GamePurchaseEmail.objects.get(code=code)
		gp.downloads += 1
		gp.save()		
	except GamePurchaseEmail.DoesNotExist:
		return mbredirect("/message/?title=Invalid purchase code&description=Invalid purchase code")		
	return renderWithNav(request, "download_full.html")

def hsbc(request, code=None):
	if request.method=="POST":
		form = HSBCForm(request.POST)
		if form.is_valid():
			c = form.cleaned_data["code"]
			if GamePurchaseEmail.objects.filter(code=c).exists():
				return mbredirect("/download/full/"+c+"/")
			else:
				form._errors["code"] = ErrorList([u"Invalid code, please double check it!"])
				return renderWithNav(request, "hsbc.html", {"hsbc_form":form})		

	else:
		form = HSBCForm(initial={"code":code})
		return renderWithNav(request, "hsbc.html", {"hsbc_form":form})

def code(request, code=None):
	if request.method=="POST":
		form = CodeForm(request.POST)
		if form.is_valid():
			c = form.cleaned_data["code"]
			email = form.cleaned_data["email"]
			if GamePurchaseEmail.objects.filter(code=c).exists():
				e = FullDownloadCodeEmailEntry(code=c, email=email, date=timezone.now())
				e.save()
				return mbredirect("/download/full/"+c+"/")
			else:
				form._errors["code"] = ErrorList([u"Invalid code, please double check it!"])
				return renderWithNav(request, "code.html", {"form":form})		
		else:
			return renderWithNav(request, "code.html", {"form":form})

	else:
		form = CodeForm(initial={"code":code})
		return renderWithNav(request, "code.html", {"form":form})		

def cohort_start(request, cohort):
	response = mbredirect("/session/try2/")
	
	tracking = tracking_cookie(request)
	if tracking is None:
		tracking = uuid.uuid1().hex
		response.set_cookie("mb_tracking", tracking,
			expires=365 * 24 * 60 * 60,
			domain=settings.SESSION_COOKIE_DOMAIN,
			secure=settings.SESSION_COOKIE_SECURE or None)

	CohortTracking.objects.filter(tracking_cookie=tracking).delete()
	ct = CohortTracking(tracking_cookie = tracking, cohort=cohort)
	ct.save()

	return response

def post_data_email_signup(email1, email2):
	return {
		"entry.1031625911": email1, 
		"entry.396703220": email2,
		"fbzx": "4528499795132730279",
	}

def newsletter(request):
	if request.method == "POST":
		email = request.POST['email']
		gdoc_url = "https://docs.google.com/forms/d/1KtJyHzzHHnXZC4pKtHYAkEPkZZ3kp0pIxg-xxfHEq50/formResponse"
		data = post_data_email_signup(email, email)
		r = requests.post(gdoc_url, data = data)
	return mbredirect("/message?title=We'll be in touch!&description=Thanks for your interest in Mathbreakers!")

def educents(request, code):
	try:
		code_model = EducentsCode.objects.get(code=code)
	except EducentsCode.DoesNotExist:
		form = EducentsCodeForm()
		return renderWithNav(request, "educents.html", {"form":form,"code":code})
	if request.method=="POST":
		form = EducentsCodeForm(request.POST)
		if form.is_valid():
			ip = get_ip(request)
			email = form.cleaned_data['email']
			#truncated_username = email[:20]
			password = form.cleaned_data['password']
			classroom_name = form.cleaned_data['classroom_name']

			user = None
			# Let's check if they already have an account and they've gone to this page
			# because they forgot / didn't know to log in
			matchusers = User.objects.filter(email=email)
			if matchusers.count() == 0:
				# They don't have an account, let's try to make one
				try:
					#user = User.objects.create_user(email, email, password)
					user = User.objects.create_user(truncated_username, email, password)
				except:
					# Must be a duplicate account
					errors = form._errors.setdefault("email", ErrorList())
					errors.append(u"That email address is already in use")
					return renderWithNav(request, "educents.html", {"form":form,"code":code})

				# This second step (logging in after successfully registering) should not ever fail.
				try:
					user = perform_signin(request, email, password)
				except:
					log_error(request)
					errors = form._errors.setdefault("email", ErrorList())
					errors.append(u"Something went wrong! Try a different email address please.")					
					return renderWithNav(request, "educents.html", {"form":form,"code":code})
				analytics.alias(request, user)
				analytics.person_set_once(user, {"$created":timezone.now()})
			else:
				errors = form._errors.setdefault("email", ErrorList())
				errors.append(u"That email address is in use, please use a different one.")					
				return renderWithNav(request, "educents.html", {"form":form,"code":code})				

			if user is None:
				log_and_email(request, "User is None somehow in educents POST handler")
				errors = form._errors.setdefault("email", ErrorList())
				errors.append(u"Something went wrong! Try a different email address please.")					
				return renderWithNav(request, "educents.html", {"form":form,"code":code})
			
			analytics.person_increment(user, "Sessions Started")
			analytics.person_append(user, "Sessions", str(timezone.now()))
			# Now that we're logged in let's make a classroom unless one exists
			ctr = None
			classroom = None

			# Okay cool let's make the classroom and relate it to this user with a CTR
			classroom = Classroom(name=classroom_name, num_students=0)
			classroom.save()
			classroom_log(classroom, "Classroom created from start")
			ctr = ClassroomTeacherRel(user=user, classroom=classroom, date=timezone.now())
			ctr.save()

			analytics.person_append(user, "Classrooms", classroom.name)
			# Set the session value so we can keep track of which classroom they're monitoring
			# currently if they have multiple classes
			request.session['classroom_id'] = classroom.id

			send_mail_threaded("New educents teacher started a session - " + str(timezone.now()), "Username: "+user.username, "robot@imaginarynumber.co", ["team@mathbreakers.com"])

			# Now find and update (or create) the session
			try:
				session = ClassroomSession.objects.get(classroom=classroom)
				session.ip = ip
				session.update_time = timezone.now()
				session.save()				
			except ClassroomSession.DoesNotExist:
				make_session(request, classroom)

			# And give them the 20
			prof = user.profile
			prof.upgraded = True
			prof.num_licenses += 20
			prof.save()

			analytics.track_event("post_teacher_start", request)

			code_model.user = user
			code_model.save()
			
			return HttpResponseRedirect("/session/status/")			
	else:
		form = EducentsCodeForm()
		return renderWithNav(request, "educents.html", {"form":form, "code":code})

@require_http_methods(['POST'])
def educentspromotion(request):
	code = request.POST['code']
	try:
		code_model = EducentsCode.objects.get(code=code)
		print code_model.user
		if code_model.user is not None:
			return mbredirect("/purchase/teacher/?error=That code has already been used!")
		code_model.user = request.user
		code_model.date_claimed = timezone.now()
		code_model.save()
		prof = request.user.profile
		prof.upgraded = True
		prof.num_licenses += 20
		prof.save()		
	except:
		return mbredirect("/purchase/teacher/?error=Invalid code")

	return mbredirect("/postpurchase/teacher/")
