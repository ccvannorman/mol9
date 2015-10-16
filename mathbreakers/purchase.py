import time
import datetime
import random
import uuid

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.conf import settings

import stripe

from mathbreakers.util import *
from mathbreakers.models import *
from mathbreakers import analytics
from mathbreakers import mbcopy


purchase_classes = {}

def register_purchase_class(cls):
	purchase_classes[cls.code] = cls
	return cls

class Purchase:
	code = ""
	post_purchase_page = "/"

	@classmethod
	def get_price_cents(cls, params):
		pd = PurchaseData.objects.get(code=cls.code)
		token = params['stripeToken']
		return pd.price * 100

	@classmethod
	def purchase_action(cls, user, params):
		raise NotImplementeError

	@classmethod
	def get_email_body(cls, token):
		return mbcopy.PURCHASE_EMAIL_RECEIPT[cls.code] % (token, )

@register_purchase_class
class FullGamePurchase(Purchase):
	code = "mbfull"
	post_purchase_page = "/postpurchase/game/" 

	@classmethod
	def purchase_action(cls, user, params):
		email = params['stripeEmail']
		gp_code = uuid.uuid1().hex
		gp = GamePurchaseEmail(email=email, time=timezone.now(), code=gp_code)
		gp.save()

		message = mbcopy.MBFULL_DLLINK % gp_code

		send_mail_threaded("Your Mathbreakers download link", message, "robot@imaginarynumber.co", [email])

@register_purchase_class
class TeacherLicensePurchase(Purchase):
	code = "teacherpurchase"
	post_purchase_page = "/postpurchase/teacher/"

	@classmethod
	def get_price_cents(cls, params):
		pd = PurchaseData.objects.get(code=cls.code)
		token = params['stripeToken']
		return pd.price * 100 * int(params["numLicenses"])		

	@classmethod
	def purchase_action(cls, user, params):	
		prof = user.profile
		prof.upgraded = True
		prof.num_licenses += int(params["numLicenses"])
		prof.save()

@register_purchase_class
class VariablePaymentPurchase(Purchase):
	code = "variablepay"
	post_purchase_page = "/postpurchase/variable/"

	@classmethod
	def get_price_cents(cls, params):
		return 100 * (float)(params["dollars"])

	@classmethod
	def purchase_action(cls, user, params):	
		pass	

stripe.api_key = ("sk_live_tvnSJ6k5vFj6oBQyzsUR6SVd", "sk_test_5shzZy4Y5x2Z7VwWmMQ4ntdG")[settings.DEBUG]

def purchase_stripe(request, code):
	token = request.POST['stripeToken']
	email = request.POST['stripeEmail']

	purchase_class = purchase_classes[code]

	price_cents = purchase_class.get_price_cents(request.POST)
	email_body = purchase_class.get_email_body(token)

	if request.user.is_authenticated():
		user = request.user
		username = user.username
	else:
		user = None
		username = ""

	pr = PurchaseRecord(
			user = user,
			stripe_token=token,
			email=email,
			code=code,
			params=str(request.POST),
			price=price_cents,
			date=timezone.now())
	pr.save()

	try:
		charge = stripe.Charge.create(
			amount=int(price_cents), # amount in cents, again
			currency="usd",
			card=token,
			description=username,
	 	)

	except stripe.CardError:
		return renderWithNav(request, "error.html", {"body":"Your card was declined."})

	analytics.track_event("purchase_" + code, request=request, data={"price_cents":int(price_cents)})

	purchase_class.purchase_action(user, request.POST)

	send_mail_threaded("Mathbreakers.com Purchase Receipt", email_body, "robot@imaginarynumber.co", [request.POST['stripeEmail']])

	message = "email %s made a purchase of %s for $%.2f" % (email, code, int(price_cents) / 100.0,)
	subject = "Payment received " + str(timezone.now())

	send_mail_threaded(subject, message, "robot@imaginarynumber.co", ["team@mathbreakers.com"])

	return HttpResponseRedirect(purchase_class.post_purchase_page)

def teacher(request):
	if not request.user.is_authenticated():
		return mbredirect("/message_teacher/?title=Must have a teacher account&description=You must have a teacher account to purchase a license")
	num_students = 0
	try:
		ctrs = ClassroomTeacherRel.objects.filter(user=request.user)
		num_classrooms = ctrs.count()
		for ctr in ctrs:
			num_students += UserClassroomAssignment.objects.filter(classroom=ctr.classroom).count()
	except:
		num_classrooms = 0

	num_licenses = request.user.profile.num_licenses

	return renderWithNav(request, "purchase_teacher.html", {
		"purchase_form":TeacherPurchaseForm(),
		"num_students": num_students,
		"num_classrooms": num_classrooms,
		"num_licenses": num_licenses
	})

def buy_full(request):
	pd = PurchaseData.objects.get(code="mbfull")
	return renderWithNav(request, "buy_full.html", {"price":"%.2f" % (pd.price)})

def pay_variable(request):
	return renderWithNav(request, "pay_variable.html")
