from mathbreakers.client import *
from mathbreakers.models import *
from django.test import TestCase, Client
import json
from django.utils.timezone import now

class ClientTestCase(TestCase):
	JSONSUCCESS = json.dumps({"success":False, "error":"Invalid parameters."})
	def setUp(self):
		User.objects.create_user("test", "test@example.com", "123123")
		# Paid user
		paid = User.objects.create_user("paid", "test@example.com", "123123")
		GamePurchase(user=paid, time=now()).save()
		#Teacher/student
		teacher = User.objects.create_user("teacher", "", "123123")
		prof = teacher.profile
		prof.upgraded = True
		prof.save()
		student = User.objects.create_user("student", "", "123123")
		classroom = Classroom(name="Test Classroom", school="Test School", grade="first", num_students=1)
		classroom.save()
		ClassroomTeacherRel(user = teacher, classroom=classroom, date=now()).save()
		UserClassroomAssignment(user=student, classroom=classroom).save()
		#Levels
		free_level = Level(name="test level", short_name="test")
		free_level.save()
		paid_level = Level(name="paid level", short_name="paid")
		paid_level.save()
		fg = LevelGroup(name="free group", upgrade_required=False)
		fg.save()
		fg.levels.add(free_level)
		
		pg = LevelGroup(name="paid group", upgrade_required=True)
		pg.save()
		pg.levels.add(paid_level)
		


	def start_session_client(self, user):
		c = Client()
		response = c.post("/client/signin/", {"username":user, "password":"123123"})
		content = json.loads(response.content)
		self.assertEqual(content['success'], True)
		c.cookies['sessionid'] = content['sessionid']
		return c

	def json_success(self, r):
		self.assertEqual(r.status_code, 200)
		content = json.loads(r.content)
		self.assertEqual(content['success'], True)
		return content

	# Test valid client signin
	def test_signin(self):
		c = Client()
		response = c.post("/client/signin/", {"username":"test", "password":"123123"})
		content = self.json_success(response)
		self.assertEqual(content.has_key("sessionid"), True)

	# Make sure a bad signin doesn't allow you to pass
	def test_bad_signin(self):
		c = Client()
		response = c.post("/client/signin/", {"username":"test", "password":"bad password"})
		content = json.loads(response.content)
		self.assertEqual(content['success'], False)
		self.assertEqual(content.has_key("sessionid"), False)

	# /client/report/level/ where the level exists alreay
	def test_report_existing_level(self):
		c = self.start_session_client("test")
		r = c.post("/client/report/level/", {"level":"test level", "stars":2})
		self.json_success(r)
		ulss = UserLevelState.objects.filter(level__name = "test level")
		self.assertEqual(ulss.exists(), True)
		self.assertEqual(ulss[0].stars, 2)

	# /client/report/level/ where the level doesn't already exist in DB
	def test_report_new_level(self):
		c = self.start_session_client("test")
		r = c.post("/client/report/level/", {"level":"test level 2", "stars":3})
		self.json_success(r)
		ulss = UserLevelState.objects.filter(level__name = "test level 2")
		self.assertEqual(ulss.exists(), True)
		self.assertEqual(ulss[0].stars, 3)

	# /client/gamestate/ for an anonymous user
	def test_gamestate_anonymous(self):
		c = Client()
		r = c.get("/client/gamestate/")
		content = self.json_success(r)
		self.assertEqual(content['purchasedlevels'], ['test level'])

	# /client/gamestate/ for a trial user
	def test_gamestate_trial_user(self):
		c = self.start_session_client("test")
		r = c.get("/client/gamestate/")
		content = self.json_success(r)
		self.assertEqual(content['purchasedlevels'], ['test level'])

	# /client/gamestate/ for a paid user
	def test_gamestate_paid_user(self):
		c = self.start_session_client("paid")
		r = c.get("/client/gamestate/")
		content = self.json_success(r)
		self.assertEqual(content['purchasedlevels'], ['paid level', 'test level'])

	# /client/gamestate/ for a (upgraded) teacher
	def test_gamestate_teacher(self):
		c = self.start_session_client("teacher")
		r = c.get("/client/gamestate/")
		content = self.json_success(r)
		self.assertEqual(content['purchasedlevels'], ['paid level', 'test level'])

	# /client/gamestate/ for a student of a (upgraded) teacher
	def test_gamestate_student(self):
		c = self.start_session_client("student")
		r = c.get("/client/gamestate/")
		content = self.json_success(r)
		self.assertEqual(content['purchasedlevels'], ['paid level', 'test level'])		

	# /client/report/heatmap/
	def test_heatmap(self):
		c = self.start_session_client("test")
		r = c.post("/client/report/heatmap/", {"heatmap":"[[1, [0,0,0], 0]]", "level":'test level'})
		self.json_success(r)
		#pt = HeatmapPoint.objects.filter(point_x=0, point_y=0, point_z=0)
		#self.assertEqual(pt.exists(), True)

	# /client/report/heatmap/ and check the activity bin
	def test_heatmap_stat_bin(self):
		c = self.start_session_client("student")
		r = c.post("/client/report/heatmap/", {"heatmap":"[[1, [0,0,0], 0]]", "level":'test level'})
		self.json_success(r)

		bins = ClassroomActivityBin.objects.filter(classroom__name="Test Classroom")
		self.assertEqual(bins.exists(), True)

		self.assertEqual(bins[0].num_seconds, 1)

	def test_version_check_old(self):
		c = self.start_session_client("student")
		r = c.get("/client/version/0.0.0.1/")
		content = json.loads(r.content)
		self.assertEqual(content["success"], True)
		self.assertEqual(content["update"], True)

	def test_version_check_future(self):
		c = self.start_session_client("student")
		r = c.get("/client/version/9.9.9.9/")
		content = json.loads(r.content)
		self.assertEqual(content["success"], True)
		self.assertEqual(content["update"], False)

	def test_version_check_current(self):
		c = self.start_session_client("student")
		from mathbreakers.client import API_VERSION
		apistr = ".".join([str(x) for x in API_VERSION])
		r = c.get("/client/version/%s/" % (apistr,))
		content = json.loads(r.content)
		self.assertEqual(content["success"], True)
		self.assertEqual(content["update"], False)		
