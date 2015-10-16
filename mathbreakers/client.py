import math
import json
import uuid
import os
import time
import datetime
import logging

from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from mathbreakers.auth import perform_signin, perform_logout
from mathbreakers.util import *
from mathbreakers.models import *

@client_post
def signin(request):
	try:
		user = perform_signin(request, request.POST['username'], request.POST['password'])
		if user:
			return json_response({"success":True, "sessionid":request.session.session_key})
		else:
			return json_response({"success":False, "error":"Invalid username or password."})
	except Exception as e:
		print e
		return json_response({"success":False, "error":"Invalid parameters."})


@client_post
def register(request):
	try:
		username = request.POST['username']
		password = request.POST['password']

		# fix bad usernames inputted by the client ...
		username2 = ''.join(c for c in username if c.islower() or c.isupper())	
		if username2 != username:
			return json_response({"success":False,"error":"User name can't use special characters."})
		if len(username) < 5:
			return json_response({"success":False,"error":"User name needs to be longer.."})
		logger.error('hi. this is a log. username and username2 are:' + username + ',' + username2)

		User.objects.create_user(username, request.POST['email'], password)
		user = perform_signin(request, username, password)
		if user:
			return json_response({"success":True, "sessionid":request.session.session_key})
		else:
			print "User successfully created but couldn't sign in!"
			return json_response({"success":False, "error":"Something went wrong"})
	except Exception as e:
		print e
		return json_response({"success":False, "error":"Invalid parameters."})
	

@client_post
@login_required
def report_topics(request):
	topicsjson = request.POST['topics'][1:-1]
	topics = json.loads(topicsjson)
	user_topics = UserTopicState.objects.filter(user=request.user).all()
	for t in topics:
		db_topic = filter(lambda x:x.topic.name == t['name'], user_topics)
		if len(db_topic) > 0:
			db_topic = db_topic[0]
		else:
			db_topic = UserTopicState.create(request.user, t['name'])
		db_topic.attempts += int(t['attempts'])
		db_topic.correct += int(t['correct'])
		db_topic.save()
	return json_response({"success":True})

@client_post
@login_required
def report_level(request):
	levelname = request.POST['level']
	stars = request.POST['stars']
	try:
		uls = UserLevelState.objects.get(level__name = levelname, user=request.user)
		uls.assigned = False
		uls.save()
	except UserLevelState.DoesNotExist:
		uls = UserLevelState.create(request.user, levelname)
	uls.stars = max(stars, uls.stars)
	uls.completed = True
	uls.checkpoint = 0
	uls.save()

	return json_response({"success":True})

def user_or_anon(request):
	if request.user.is_authenticated():
		return request.user

	ip = request.META.get('REMOTE_ADDR', None)
	newname = "anon_" + ip
	try:
		return User.objects.create_user(newname, "anon@example.com", "newtonatwork")	
	except:
		return User.objects.get(username=newname)

API_VERSION = (1,0,0,4)

def need_new_version(versionstr):
	try:
		versionbits = [int(v) for v in versionstr.split(".")]
		for x in range(4):
			if versionbits[x] > API_VERSION[x]:
				return False
			if versionbits[x] < API_VERSION[x]:
				return True
	except:
		return True
	return False

@client_get
def version(request, versionstr):
	need_api_update = need_new_version(versionstr)
	# TODO: Add forced update for non-API matters like important game version updates
	need_update = need_api_update
	obj = {"version":".".join([str(x) for x in API_VERSION]), "update":need_update, "success":True}
	return json_response(obj)

@client_get
def client_message(request, versionstr):
	# TODO: write client side for this
	obj = {"display":False, "message":"A new version is available!", "link":"https://mathbreakers.com/download"}
	return json_response(obj)

@client_post
def heatmap(request):
	user = user_or_anon(request)
	try:
		heatmapjson = request.POST['heatmap']
	except:
		log_error(request)
		return json_response({"success":False})

	pts = json.loads(heatmapjson)
	# pt format is [type, [x,y,z], timestamp]
	#for pt in pts:
	#	td = timezone.now() + datetime.timedelta(seconds=int(pt[2]))
	#	hp = HeatmapPoint(user=user, point_type=pt[0],
	#		point_x=pt[1][0], point_y=pt[1][1], point_z=pt[1][2],
	#		time=td, level_name = request.POST['level'])
	#	hp.save()

	profile = user.profile
	profile.playtime += len(pts)
	profile.save()
	ucas = UserClassroomAssignment.objects.filter(user=user)
	if len(ucas) > 0:
		nowbin = timezone.now()
		nowbin = nowbin.replace(microsecond=0, second=0, minute=0)

		# Record classroom activity for this "time bin"
		for uca in ucas:
			room = uca.classroom
			cab = None
			matching = ClassroomActivityBin.objects.filter(classroom=room, date=nowbin)
			if matching.exists():
				cab = matching[0]
			else:
				cab = ClassroomActivityBin(classroom=room, date=nowbin, num_seconds=0)
			cab.num_seconds += len(pts)
			cab.save()

	return json_response({"success":True})

@client_post
def menuclicks(request):
	user = user_or_anon(request)
	try:
		menuclicks = request.POST['menuclicks']
	except:
		log_error(request)
		return json_response({"success":False})

	pts = json.loads(menuclicks)
	# pt format is [type, name, timestamp]
	for pt in pts:
		td = timezone.now() + datetime.timedelta(seconds=int(pt[2]))
		hp = GameMenuClick(user=user, click_type=pt[0],
			button=pt[1], time=td)
		hp.save()
	return json_response({"success":True})

@client_post
@login_required
def upload_image(request):
	form = ImageUploadForm(request.POST, request.FILES)
	if form.is_valid():	
		img = GalleryImage(owner=request.user, image_file=request.FILES['file'], gallery=form.cleaned_fields.gallery)
		img.save()

	return json_response({"success":True})

@client_post
@login_required
def refer_email(request):
	email_addr = request.POST['email']
	code = uuid.uuid1().hex
	er = EmailReferral(email=email_addr, clicked=False, code=code, sender=request.user)
	er.save()

	send_mail("Try Mathbreakers!",
		"Your friend with the username " + request.user.username + " wants you to try out Mathbreakers! Here's a link: http://mathbreakers.com/referred/" + code,
		"try@imaginarynumber.co",
		[email_addr])

	return json_response({"success":True})


@client_get
def assignments(request):
	user = user_or_anon(request)
	assigned = []
	for uls in UserLevelState.objects.filter(user=user):
		if uls.assigned:
			assigned.append(uls.level.name)
	return json_response({"success":True, "assigned":assigned})

@client_get
def gamestate(request):
	user = user_or_anon(request)
	purchases = {"full_game":False, "deluxe_game":False}
	db_groups = LevelGroup.objects.all()
	try:
		gp = GamePurchase.objects.get(user=user)
		purchases["full_game"] = True
		if gp.deluxe:
			purchases["deluxe_game"] = True
	except GamePurchase.DoesNotExist:
		pass

	def levels_in_groups(groups):
		levels = []
		for group in groups:
			for lvl in group.levels.all():
				levels.append(lvl.name)
		return levels

	beaten = []
	for uls in UserLevelState.objects.filter(user=user):
		if uls.completed:
			beaten.append(uls.level.name)

	levels = []
	# What lesson plans are free?
	free_groups = LevelGroup.objects.filter(upgrade_required=False)
	levels.extend(levels_in_groups(free_groups))

	# What lesson plans do I have purchased?
	if user.profile.upgraded:
		levels.extend(levels_in_groups(LevelGroup.objects.all()))

	if GamePurchase.objects.filter(user=user).count() > 0:
		levels.extend(levels_in_groups(LevelGroup.objects.all()))

	# What lesson plans does my teacher have unlocked?
	try:
		classroom = UserClassroomAssignment.objects.get(user=user).classroom
		teacher = ClassroomTeacherRel.objects.get(classroom=classroom).user	
		if teacher.profile.upgraded:
			levels.extend(levels_in_groups(LevelGroup.objects.all()))
	except:
		pass
	levels = list(set(levels))
	return json_response({"success":True, "gamePurchases":purchases, "purchasedlevels":levels, "beatenlevels":beaten})


@client_post
@login_required
def screenshot(request):
	up_file = request.FILES['image']
	subpath = request.user.username + "." + unicode(time.time()) + ".png"
	path = os.path.join(settings.MEDIA_ROOT, subpath)
	destination = open(path, 'wb+')
	for chunk in up_file.chunks():
		destination.write(chunk)
	destination.close()
	img = GalleryImage(owner = request.user, image_file=subpath, gallery="default")
	img.save()
	return json_response({"success":True})

@client_get
def notice_image(request):
	f = open(os.path.join(settings.STATIC_ROOT,"img/nav_logo.png"), "rb")
	image_data = f.read()
	f.close()
	return HttpResponse(image_data, content_type="image/png")


@client_get
def roboterra_login(request):
	ip = get_ip(request)
	rl = RoboterraLogin(ip=ip, time=timezone.now())
	rl.save()
	return json_response({"success":True})

@client_get
@login_required
def skills(request):
	obj = {}
	for uas in UserAdaptiveSkill.objects.filter(user=request.user):
		obj[uas.skill_id] = uas.skill_level

	return json_response({"success":True, "skills":obj})

@client_post
@login_required
def report_skills(request):
	skills_json = request.POST['skills']
	skills = json.loads(skills_json[1:-1])
	for (sid,level) in skills.items():
		matching = UserAdaptiveSkill.objects.filter(user=request.user, skill_id=sid)
		if matching.exists():
			uas = matching[0]
			uas.skill_level = float(level)
			uas.save()
		else:
			uas = UserAdaptiveSkill(user=request.user, skill_id=sid, skill_level=float(level))
			uas.save()
	return json_response({"success":True})


def get_character(request):
	cs = Character.objects.filter(user=request.user)
	if cs.count() == 0:
		c = Character(user=request.user, gems=-1)
		c.save()
		return c
	else:
		return cs.first()

@client_get
@login_required
def gems(request):
	gems = get_character(request).gems
	return json_response({"success":True, "gems":gems})

@client_post
@login_required
def report_gems(request):
	num_gems = request.POST['gems']
	c = get_character(request)
	c.gems = int(num_gems)
	c.save()
	return json_response({"success":True})

@client_get
@login_required
def costume(request):
	items = []
	for item in InventoryItem.objects.filter(user=request.user):
		items.append({"item":item.item_name, "equipped":item.equipped, "variation":item.variation})
	return json_response({"success":True, "costume":items})


@client_post
@login_required
def report_costume(request):
	items_json = request.POST['costume']

	items = json.loads(items_json)
	for item in items:
		item_name = item['name']
		equipped = item['equipped']
		variation = item.get('variation', 0)
		matching = InventoryItem.objects.filter(user=request.user, item_name=item_name)
		if matching.exists():
			m = matching[0]
			m.equipped = equipped
			m.variation = variation
			m.save()
		else:
			item = InventoryItem(user=request.user, item_name=item_name, equipped=equipped, variation=variation)
			item.save()

	return json_response({"success":True})	

@client_get
@login_required
def inventory(request):
	inventory = []
	for inv in NewInventoryItem.objects.filter(user=request.user):
		inventory.append({"name":inv.item_type, "position":inv.equip_slot, "properties":inv.properties})
	return json_response({"success":True, "inventory":inventory})

@client_post
@login_required
def report_inventory(request):
	inventory_json = request.POST['inventory']
	inventory = json.loads(inventory_json)["items"]
	NewInventoryItem.objects.filter(user=request.user).delete()
	for inv in inventory:
		nii = NewInventoryItem(user=request.user, item_type = inv["name"], equip_slot=inv["position"], properties=inv["properties"])
		nii.save()	
	return json_response({"success":True})
	
@client_get
@login_required
def checkpoint(request):
	if 'level' in request.POST:
		level = request.POST['level']
		try:
			uls = UserLevelState.objects.get(level__name=level, user=request.user)
			return json_response({"success":True, "checkpoint":uls.checkpoint})
		except UserLevelState.DoesNotExist:
			return json_response({"success":True, "checkpoint":0})
	else:
		checkpoints = [
			{"level":uls.level.name, "checkpoint":uls.checkpoint}
			for uls in UserLevelState.objects.filter(user=request.user)
		]
		return json_response({"success":True, "checkpoints":checkpoints})

@client_post
@login_required
def report_checkpoint(request):
	level = request.POST['level']
	checkpoint = request.POST['checkpoint']
	uls = None
	try:
		uls = UserLevelState.objects.get(level__name=level, user=request.user)
	except UserLevelState.DoesNotExist:
		uls = UserLevelState.create(request.user, level)
	uls.checkpoint = int(checkpoint)
	uls.save()
	return json_response({"success":True})


@client_get
@login_required
def legacy_costume_gems_inventory(request):
	items = []
	for item in InventoryItem.objects.filter(user=request.user):
		items.append({"item":item.item_name, "equipped":item.equipped, "variation":item.variation})		
	inventory = []
	for inv in NewInventoryItem.objects.filter(user=request.user):
		inventory.append({"name":inv.item_type, "position":inv.equip_slot, "properties":inv.properties})			
	gems = get_character(request).gems
	return json_response({"success":True, "gems":gems, "items":items, "inventory":inventory})	

@client_post
@login_required
def legacy_report_costume_gems_inventory(request):
	items_json = request.POST['items']
	inventory_json = request.POST.get('inventory', None)
	num_gems = request.POST.get('gems', None)

	

	items = json.loads(items_json)
	for item in items:
		item_name = item['name']
		equipped = item['equipped']
		variation = item.get('variation', 0)
		matching = InventoryItem.objects.filter(user=request.user, item_name=item_name)
		if matching.exists():
			m = matching[0]
			m.equipped = equipped
			m.variation = variation
			m.save()
		else:
			item = InventoryItem(user=request.user, item_name=item_name, equipped=equipped, variation=variation)
			item.save()

	if inventory_json is not None:
		inventory_json = inventory_json.replace("}{", "},{")
		inventory = json.loads(inventory_json)["items"]
		NewInventoryItem.objects.filter(user=request.user).delete()
		for inv in inventory:
			nii = NewInventoryItem(user=request.user, item_type = inv["name"], equip_slot=inv["position"], properties=inv["properties"])
			nii.save()	

	if num_gems is not None:
		c = get_character(request)
		c.gems = int(num_gems)
		c.save()

	return json_response({"success":True})	
