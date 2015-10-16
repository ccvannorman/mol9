import uuid

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib import auth

from mathbreakers.forms import *
from mathbreakers.auth import perform_signin, perform_logout
from mathbreakers.models import *
from mathbreakers.util import *


def redeemcode(request, code=None):
	print code
	if request.method != 'POST':
		try:
			pr = PreorderRegistration.objects.get(code=code)
			if pr.user is not None:
				return renderWithNav(request, '404.html')	
		except:
			return renderWithNav(request, '404.html')
		return renderWithNav(request, 'redeempreorder.html', {"code":code, "form":RedeemPreorderForm()})

	# it's POST.
	try:
		form = RedeemPreorderForm(request.POST)
		message = ""
		code = request.POST['code']
		if form.is_valid():
			message = "\n".join([str(it[0]) + ": " + str(it[1]) for it in form.cleaned_data.items()])
			#message = str(form.cleaned_data)
			send_mail("mathbreakers preorder survey results", message, "robot@imaginarynumber.co", ["team@mathbreakers.com"])
		else:
			message = str(request.POST)
			return renderWithNav(request, 'redeempreorder.html', {"code":code, "form":form})

		pr = PreorderRegistration.objects.get(code=request.POST['code'])
		if pr.user is not None:
			return renderWithNav(request, '404.html')	
		
		if not GamePurchase.objects.filter(user=request.user).exists():
			gp = GamePurchase(user=request.user, time=timezone.now())
			gp.save()

		pr.user = request.user
		pr.response = message
		pr.save()

		code = uuid.uuid1().hex
		GamePurchaseEmail(email="", code=code, time=timezone.now()).save()
	except:
		return renderWithNav(request, "404.html")

	return mbredirect("/download/full/" + code)

def preorder(request):
	return renderWithNav(request, "preorder.html")
