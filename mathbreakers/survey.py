from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required

from mathbreakers.models import *
from mathbreakers.util import *

def survey(request):
	sid = request.GET['surveyid']
	rid = request.GET['responseid']
	survey = EmailSurvey.objects.get(id=sid)
	response = EmailSurveyResponse.objects.get(id=rid)
	survey.total += 1
	response.num += 1
	survey.save()
	response.save()

	return HttpResponseRedirect(
		"/message/?title="
		+ response.post_answer_message_title
		+ "&description=" 
		+ response.post_answer_message_description)