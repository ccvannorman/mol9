import json
import time
import uuid

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.utils import timezone

import requests

from mathbreakers.forms import *
from mathbreakers.util import *
from mathbreakers.models import *
from mathbreakers.auth import perform_signin, perform_logout
from mathbreakers import mbcopy
from mathbreakers import analytics


def post_data_download_survey(hear_about_us, email1, email2, platform):
	return {
		"entry.1769026509": hear_about_us,
		"entry.638716550": email1,
		"entry.2076140035": email2,
		"entry.265792676": platform,
		"fbzx": "-8844916261623649196",
	}

def post_data_email_signup(email1, email2):
	return {
		"entry.1031625911": email1, 
		"entry.396703220": email2,
		"fbzx": "4528499795132730279",
	}

def createaccount(request):
	if request.method == 'POST':
		form = CreateAccountForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = User.objects.create_user(username, 'none@none.com', password)
			if user is None:
				print "User failed to create despite clean fields"
				return json_response({"result":"error", "errors":{"error": "User failed to create despite clean fields"}})
			user = perform_signin(request, username, password)
			if user is None:
				print "User was created but login failed"
				return json_response({"result":"error", "errors":{"error": "User was created but login failed"}})
			return json_response({'result':'success', 'username':username})
		else:
			return json_response({'result':'error', 'errors':form.errors})
		
	else:
		return json_response({'result':'error', 'errors':{'method':'Method must be POST'}})

def signin(request):
	if request.method == 'POST':
		form = SignInForm(request.POST)
		if form.is_valid():
			user = None
			try:
				#truncated_username = form.cleaned_data['username'][:30]
				#user = perform_signin(request, truncated_username, form.cleaned_data['password'])
				user = perform_signin(request, form.cleaned_data['username'], form.cleaned_data['password'])
			except:
				user = None
			if user:
				return json_response({'result':'success', 'username':user.username})
			else:
				return json_response({'result':'error', 'errors':{"error":"Wrong username or password!"}})
		else:
			return json_response({'result':'error', 'errors':form.errors})
	else:
		return json_response({'result':'error', 'errors':{'method':'Method must be POST'}})			

def signup(request):
	if request.method == 'POST':
		returnObj = {}
		form = SignupForm(request.POST)
		if form.is_valid():
			print str(form.cleaned_data)
			message = str(form.cleaned_data)
			#send_mail("mathbreakers.com email signup", message, "robot@imaginarynumber.co", ["morganquirk@gmail.com"])
			returnObj['result'] = 'success'
			gdoc_url = "https://docs.google.com/forms/d/1KtJyHzzHHnXZC4pKtHYAkEPkZZ3kp0pIxg-xxfHEq50/formResponse"
			data = post_data_email_signup(form.cleaned_data['email'], form.cleaned_data['parent_email'])
			r = requests.post(gdoc_url, data = data)

		else:
			returnObj['result'] = 'error'
			returnObj['errors'] = form.errors
		return json_response(returnObj)
	else:
		return json_response({'result':'error', 'errors':{'method':'Method must be POST'}})

def download(request, platform):
	if request.method == 'POST':
		returnObj = {}
		form = DownloadForm2(request.POST)
		if form.is_valid():
			message = str(form.cleaned_data)
			if not request.user.is_anonymous():
				request.user.email = form.cleaned_data['email']
				prof = request.user.profile
				prof.send_news = form.cleaned_data['sendstuff']
				prof.save()
				request.user.save()
			#else:
				#send_mail("Anonymous mathbreakers.com download", message, "robot@imaginarynumber.co", ["team@mathbreakers.com"])
			returnObj['result'] = 'success'
			if platform == "mac":
				returnObj['url'] = '/static/builds/latest/mathbreakers_mac.zip'
			else:
				returnObj['url'] = '/static/builds/latest/mathbreakers_windows.zip'

			gdoc_url = "https://docs.google.com/forms/d/19nnHJID3OwZsOsIxymsSmORnua58wTBsh8P2b1uqkfs/formResponse"
			sp_email = form.cleaned_data['email']
			if form.cleaned_data['sendstuff']:
				sp_email += " *"
			data = post_data_download_survey('...', sp_email, '...', platform)
			r = requests.post(gdoc_url, data = data)

		else:
			returnObj['result'] = 'error'
			returnObj['errors'] = form.errors;
		return json_response(returnObj)
	else:
		return json_response({'result':'error', 'errors':{'method':'Method must be POST'}})		

def contestregister(request):
	if request.method == 'POST':
		returnObj = {}
		form = ContestRegistrationForm(request.POST)
		if form.is_valid():
			print str(form.cleaned_data)
			message = str(form.cleaned_data)
			#send_mail("mathbreakers.com contest registration", message, "robot@mathbreakers.com", ["morganquirk@gmail.com"])
			returnObj['result'] = 'success'
		else:
			returnObj['result'] = 'error'
			returnObj['errors'] = form.errors;
		return json_response(returnObj)
	else:
		return json_response({'result':'error', 'errors':{'method':'Method must be POST'}})		

def createteacheraccount(request):
	if request.method == 'POST':
		form = TeacherSignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			user = User.objects.create_user(username, email, password)
			profile = user.profile
			profile.upgraded = True
			profile.save()
			newclass = Classroom(name = form.cleaned_data['classroom_name'], school=form.cleaned_data['school'], grade=form.cleaned_data['grade_level'], num_students=0)
			newclass.save()
			ct = ClassroomTeacherRel(user=user, classroom=newclass, date=timezone.now())
			ct.save()
			user.first_name = form.cleaned_data['first']
			user.last_name = form.cleaned_data['last']
			user.save()
			bodytext = mbcopy.TEACHER_ACCOUNT_CREATED_EMAIL[1].format(form.cleaned_data['username'],form.cleaned_data['password'])
			send_mail_threaded(mbcopy.TEACHER_ACCOUNT_CREATED_EMAIL[0], bodytext, "robot@imaginarynumber.co", [form.cleaned_data['email']])
			if user is None:
				print "User failed to create despite clean fields"
				return json_response({"result":"error", "errors":{"error": "User failed to create despite clean fields"}})
			user = perform_signin(request, username, password)
			if user is None:
				print "User was created but login failed"
				return json_response({"result":"error", "errors":{"error": "User was created but login failed"}})
			return json_response({'result':'success', 'username':username})
		else:
			return json_response({'result':'error', 'errors':form.errors})
	else:
		return json_response({'result':'error', 'errors':{'method':'Method must be POST'}})

def convertteacheraccount(request):
	if request.method == 'POST':
		form = TeacherConvertForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			request.user.first_name = form.cleaned_data['first']
			request.user.last_name = form.cleaned_data['last']
			request.user.email = email
			request.user.save()
			profile = request.user.profile
			profile.upgraded = True
			profile.save()
			newclass = Classroom(name = form.cleaned_data['classroom_name'], school=form.cleaned_data['school'], grade=form.cleaned_data['grade_level'], num_students=0)
			newclass.save()
			ct = ClassroomTeacherRel(user=request.user, classroom=newclass, date=timezone.now())
			ct.save()
			return json_response({'result':'success'})
		else:
			return json_response({'result':'error', 'errors':form.errors})
		
	else:
		return json_response({'result':'error', 'errors':{'method':'Method must be POST'}})

button_analytics_tracking = {
	'license':'click_purchase_license_nav',
	'teacherbuy':'click_purchase_license_status',
	'dl_free_win':'click_dl_free_win',
	'dl_free_mac':'click_dl_free_mac',
	'dl_free_linux':'click_dl_free_linux',
	'dl_full_win':'click_dl_full_win',
	'dl_full_mac':'click_dl_full_mac',
	'dl_full_linux':'click_dl_full_linux',
}

def buttonlog(request, name):
	if "fakelogin" in request.COOKIES:
		return json_response({'result':'success'})
	ip = request.META.get('REMOTE_ADDR', None)
	user = None
	if request.user.is_authenticated():
		user = request.user
	bl = ButtonLog(
		page="",
		name=name,
		user=user,
		ip=ip,
		time=timezone.now(),
		tracking_cookie=tracking_cookie(request))
	bl.save()
	if name in button_analytics_tracking:
		event = button_analytics_tracking[name]
		analytics.track_event(event, request=request)
	return json_response({'result':'success'})

def campform(request):
	if request.method == 'POST':
		form = CampSignupForm(request.POST)
		if form.is_valid():
			purchaseid = str(uuid.uuid1())
			ticket_type = form.cleaned_data['ticket'] == "True"
			name = ("Camp Ticket", "Camp Ticket + Kit")[ticket_type]
			desc = "Camp Ticket"
			price = (360, 425)[ticket_type]
			if not request.user.is_anonymous() and request.user.is_superuser:
				price = (0.01, 0.02)[ticket_type]
			code = ("camp", "campandkit")[ticket_type]
			import jwt
			cakeToken = jwt.encode(
				{
				    "iss" : "17845422735024024747",
				    "aud" : "Google",
				    "typ" : "google/payments/inapp/item/v1",
				    "exp" : int(time.time()+1800),
				    "iat" : int(time.time()),
				    "request" :{
				      "name" : name,
				      "description" : desc,
				      "price" : price,
				      "currencyCode" : "USD",
				      "sellerData" : "user_id:1224245,offer_code:3098576987,affiliate:aksdfbovu9j",
				      "code" : code,
				      "purchaseid": purchaseid,
				      "user" : None
					}
				}, "D69_jY6roAG5ZhrkAlkUKw")	

			cs = CampSignup(
				parent_name = form.cleaned_data['parent_name'],
				parent_email = form.cleaned_data['parent_email'],
				child_name = form.cleaned_data['child_name'],
				child_age = form.cleaned_data['child_age'],
				session = form.cleaned_data['session'],
				plus_kit = ticket_type,
				paid=False,
				purchaseid = purchaseid
				)
			cs.save()
			return json_response({'result':'success', 'token':cakeToken})
		else:
			return json_response({'result':'error', 'errors':form.errors})
	else:
		return json_response({'result':'error', 'errors':{'method':'Method must be POST'}})			
