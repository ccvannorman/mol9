from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required

from mathbreakers.models import *
from mathbreakers.util import *

def change_password(request):
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST, request=request)
		if form.is_valid():
			request.user.set_password(form.cleaned_data['new_password'])
			request.user.save()
			return HttpResponseRedirect('/message/?title=Password Changed&description=Next time you login you will have to use your new password.')
		else:
			return renderWithNav(request, "settings.html", {"change_password_form": form})

def settings(request):
	pw_form = ChangePasswordForm(request=request)
	return renderWithNav(request, "settings.html", {
		"change_password_form": pw_form
	})