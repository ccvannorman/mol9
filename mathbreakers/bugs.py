from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt

from mathbreakers.models import *
from mathbreakers.util import *
from mathbreakers.su import *

@csrf_exempt
def report(request):
	# report_text = request.GET['report']
	report_text = request.POST['report']
	bug_list = report_text.split("|") #request.POST['report'].split('|')
#		
	bug = Bug(
		description = bug_list[0],
		date = bug_list[1],
		level = bug_list[2],
		position = bug_list[3],
		vers = bug_list[4],
		user = bug_list[5],
		session = bug_list[6])
	bug.save()

	return json_response({report_text:True})

@su_required
def show(request):
	bugs = [b for b in Bug.objects.all()]
	bugs.reverse()

	return renderWithNav(request, "bugs.html", {"bugs":bugs})
