import os
import math

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from mathbreakers.models import *
from mathbreakers.util import *


SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

def grade(request):
	f = open(os.path.join(SITE_ROOT, "cc/cc-grade.json"), "r")
	data = f.read()
	f.close()
	return HttpResponse(data, content_type="application/json")

def category(request):
	f = open(os.path.join(SITE_ROOT, "cc/cc-categories.json"), "r")
	data = f.read()
	f.close()
	return HttpResponse(data, content_type="application/json")

def table(request):
	pass

gradenames = [
	"Kindergarten",
	"First Grade",
	"Second Grade",
	"Third Grade",
	"Fourth Grade",
	"Fifth Grade",
	"Sixth Grade",
	"Seventh Grade",
	"Eighth Grade",
]

def rgb_to_hex(*rgb):
	return '%02x%02x%02x' % rgb

def gen_color(index, max_index):
	i = (float(index) / float(max_index) * 3.14159 * 1.8) + 2.9
	r = math.cos(-i) * 50 + 205
	g = math.cos(-i + 2) * 50 + 205
	b = math.cos(-i + 4) * 50 + 205
	return rgb_to_hex(r,g,b)

def get_cc_table():
	f = open(os.path.join(SITE_ROOT, "cc/cc-table-annotated.json"), "r")
	data = json.loads(f.read())
	f.close()
	cats = []
	i = 0
	for c in data['categories']:
		cats.append({"name": c, "color": gen_color(i, len(data['categories']))})
		i += 1
	table = []
	i = 0
	for g in data['table']:
		grade_cats = []
		j = 0
		for cat in g:
			grade_cats.append({"color": gen_color(j, len(cats)), "data":cat})
			j += 1
		table.append({"name": gradenames[i], "data":grade_cats})
		i += 1
	return (cats, table)

def abbreviate(lesson):
	lesson['shortname'] = lesson['name'].split(".", 3)[-1]
	return lesson

def index(request):
	cats, table = get_cc_table()
	for g in table: 
		for c in g['data']:
			lessons = c['data']
			c['data'] = [abbreviate(lesson) for lesson in lessons]
	return renderWithNav(request, "commoncore.html", {"categories":cats, "grades":table})

def full(request):
	cats, table = get_cc_table()
	return renderWithNav(request, "commoncore_full.html", {"categories":cats, "grades":table})