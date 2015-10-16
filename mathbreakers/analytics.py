import json
import time
import datetime
import calendar
import math
import base64

from django.conf import settings
from django.utils import timezone

import requests
import pytz
from mixpanel import Mixpanel

from mathbreakers.util import *
from mathbreakers.models import *

def merge_points(pts, merge):
	#xs = [pt[1][0] for pt in pts]
	#ys = [pt[1][1] for pt in pts]
	#zs = [pt[1][2] for pt in pts]

	#box = (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))
	#scales = (box[1]-box[0], box[3] - box[2], box[5] - box[4])

	pos_pts = {}

	for pt in pts:
		x = int(pt[1][0] / merge) * merge + merge / 2
		y = int(pt[1][1] / merge) * merge + merge / 2
		z = int(pt[1][2] / merge) * merge + merge / 2
		if pos_pts.has_key((x,y,z)):
			pos_pts[(x,y,z)][2] += 1
			pos_pts[(x,y,z)][3] += pt[3]
		else:
			pos_pts[(x,y,z)] = [pt[0], [x,y,z], 1.0, pt[3], ""]

	for pt in pts:
		pt[3] = pt[3] / pt[2]

	ret = pos_pts.values()
	ret.sort(lambda x,y:cmp(x[3], y[3]))
	return ret

def heatmap(request, levelname):
	querySet = HeatmapPoint.objects.filter(level_name=levelname)

	if request.GET.has_key('type'):
		querySet = querySet.filter(point_type=request.GET['type'])

	if request.GET.has_key('random'):
		querySet = querySet.order_by('?')
	else:
		querySet = querySet.order_by('time')

	if request.GET.has_key('username'):
		user = User.objects.get(username=request.GET['username'])
		querySet = querySet.filter(user=user)

	start = int(request.GET.get('start', 0))
	count = int(request.GET.get('count', 1000))

	pts = querySet[start:start+count]
	
	retpts = []
	for pt in pts:
		ptobj = [pt.point_type, [pt.point_x, pt.point_y, pt.point_z], 1.0, calendar.timegm(pt.time.utctimetuple()), pt.user.username]
		retpts.append(ptobj)

	merge = int(request.GET.get('merge', 1))
	if merge > 1:
		retpts = merge_points(retpts, merge)

	return json_response({"success":True, "points":retpts})


mp = Mixpanel(settings.MIXPANEL_TOKEN)

amazon_ips = [
	"172.31.4.44",
	"172.31.2.92",
]

amazon_ip_start = "172.31."

def gen_backdated_event(date, event_name, request=None, tracking_cookie=None, user=None, data=None):
	trackid = get_track_id(request, tracking_cookie, user)

	evttime = calendar.timegm(date.utctimetuple())

	event = {
		"event": event_name,
		"properties":{
			"distinct_id": trackid,
			"time": evttime,
			"token": settings.MIXPANEL_TOKEN
		}
	}

	return event 

MIXPANEL_START_DATE = datetime.datetime(year=2015,month=3,day=20,hour=12,tzinfo=pytz.timezone("US/Pacific"))

def track_backdated_cookie_events(objs):
	batches = int(math.ceil(len(objs) / 50.0))
	url = "http://api.mixpanel.com/import/"

	for i in range(batches):
		batch = []
		skipped = 0
		for obj in objs[i * 50 : (i+1) * 50]:
			if obj[0] < MIXPANEL_START_DATE:
				batch.append(gen_backdated_event(obj[0], obj[1], tracking_cookie=obj[2]))
			else:
				skipped += 1
		events_json = json.dumps(batch)
		print "sending " + str(len(batch)) + " events. Skipped " + str(skipped) + "."
		full_url = url + "?data="+base64.b64encode(events_json) + "&api_key=" + settings.MIXPANEL_API
		r = requests.get(full_url)
		print "status: " + str(r.status_code)

def track_event(event_name, request=None, tracking_cookie=None, user=None, data=None):
	if settings.RUNNING_TESTS:
		return

	if request and get_ip(request).startswith(amazon_ip_start):
		return

	trackid = get_track_id(request, tracking_cookie, user)

	mp.track(trackid, event_name, data)

def get_track_id(request=None, tracking_cookie=None, user=None):
	trackid = None
	if request is not None:
		if not request.user.is_anonymous():
			user = request.user
			
		elif request.COOKIES.has_key("mb_tracking"):
			tracking_cookie = request.COOKIES["mb_tracking"]

		else:
			trackid = "ip_" + get_ip(request)

	if user is not None:
		trackid = "user_" + str(user.username)

	elif tracking_cookie is not None:
		trackid = "cookie_" + tracking_cookie	

	return trackid

def alias(request, user):
	if settings.RUNNING_TESTS:
		return

	new_trackid = "user_" + str(user.username)
	if request.COOKIES.has_key("mb_tracking"):
		old_trackid = "cookie_" + str(request.COOKIES["mb_tracking"])
	else:
		old_trackid = "ip_" + get_ip(request)
	mp.alias(new_trackid, old_trackid)

def person_update(user, data):
	if settings.RUNNING_TESTS:
		return

	trackid = get_track_id(user = user)
	data["$email"] = user.email
	data["$username"] = user.email
	data["$name"] = user.email
	data["licenses"] = user.profile.num_licenses
	mp.people_set(trackid, data)

def person_set_once(user, data):
	if settings.RUNNING_TESTS:
		return

	person_update(user, {})

	mp.people_set_once(get_track_id(user = user), data)

def person_increment(user, field, amt=1):
	if settings.RUNNING_TESTS:
		return

	person_update(user, {})

	mp.people_increment(get_track_id(user = user), {field: amt})

def person_append(user, field, value):
	if settings.RUNNING_TESTS:
		return	

	person_update(user, {})

	mp.people_append(get_track_id(user = user), {field: value})