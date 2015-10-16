from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt

import mathbreakers.models
from mathbreakers.util import *

def deleterow(request):
	model = request.POST['model']
	col = request.POST['col']
	val = request.POST['val']
	mymodel = models.get_model('mathbreakers', model)
	mymodel.objects.filter(**{col:val}).delete()
	return json_response({"message" : "Deleted " + val + " from " + model, "success" : True})


def addrow(request):
	model = request.POST['model']
	mymodel = models.get_model('mathbreakers', model)
	mymodel.objects.create()
	return json_response({"message" : "Created new row", "success" : True})

def modifyrow(request):
	model = request.POST['model']
	match_col = request.POST['match_col']
	match_val = request.POST['match_val']
	mod_col = request.POST['mod_col']
	mod_val = request.POST['mod_val']
	mymodel = models.get_model('mathbreakers', model)	
	obj_to_mod = mymodel.objects.filter(**{match_col:match_val})[0]
	if not obj_to_mod:
		obj_to_mod = mymodel.objects.create(**{match_col:match_val,mod_col:mod_val})
	if not obj_to_mod:
		return json_response({"message" : "something went wrong..couldn't find OR create a row matching " + match_val + " at columb " + match_col + " in table " + model, "success" : False})
	try: setattr(obj_to_mod,mod_col,mod_val)
	except: return json_response({"error" : "Wrong data type: "+mod_val+"doesn't fit into "+mod_col + " in table  " + model, "success" : False})
	obj_to_mod.save()
	return json_response({"message" : "Modified " + val + " from " + model, "success" : True})

