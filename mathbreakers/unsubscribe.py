from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt
from mathbreakers.models import *
from mathbreakers.util import *
from django.utils import timezone
import datetime
@csrf_exempt
def unsub(request):
	email = request.GET.get('email',None)
	unsub = Unsubscribed(email=email,date=timezone.now())
	unsub.save()
	return renderWithNav(request, "unsubscribe.html", {"email":email})



