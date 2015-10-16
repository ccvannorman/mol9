from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt

from mathbreakers.util import *
import mathbreakers.models

@csrf_exempt
def deleterow(request):
	model = request.GET['model']
	col = request.GET['col']
	val = request.GET['val']
	mymodel = models.get_model('mathbreakers', model)
	mymodel.objects.filter(**{col:val}).delete()
	return json_response({"message" : "Deleted " + val + " from " + model, "success" : True})


@csrf_exempt
def addrow(request):
	model = request.GET['model']
	mymodel = models.get_model('mathbreakers', model)

