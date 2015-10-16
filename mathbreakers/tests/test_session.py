from mathbreakers.client import *
from mathbreakers.models import *
from django.test import TestCase, Client
import json
from django.utils.timezone import now

class SessionTestCase(TestCase):
	JSONSUCCESS = json.dumps({"success":False, "error":"Invalid parameters."})
	def setUp(self):
		User.objects.create_user("test", "test@example.com", "123123")

		#Teacher/student
		teacher = User.objects.create_user("teacher", "", "123123")
		prof = teacher.profile
		prof.upgraded = True
		prof.save()
		student_oldname = User.objects.create_user("john", "", "default")
		classroom = Classroom(name="Test Classroom", school="Test School", grade="first", num_students=1)
		classroom.save()
		self.classroom_id = classroom.id
		ClassroomTeacherRel(user = teacher, classroom=classroom, date=now()).save()
		UserClassroomAssignment(user=student_oldname, classroom=classroom).save()

		#Expired teacher/student
		teacher = User.objects.create_user("teacherx", "", "123123")
		prof = teacher.profile
		prof.num_licenses=0
		prof.save()
		student_oldname = User.objects.create_user("johnx", "", "default")
		student_oldname.profile.playtime=9000
		student_oldname.profile.save()
		classroom = Classroom(name="Test Classroom X", school="Test School X", grade="first", num_students=1)
		classroom.save()
		self.classroom_x_id = classroom.id
		ClassroomTeacherRel(user = teacher, classroom=classroom, date=now()).save()
		UserClassroomAssignment(user=student_oldname, classroom=classroom).save()	
		ClassroomActivityBin(classroom=classroom, num_seconds=9000, date=timezone.now()).save()

		#Partially evaluated trial teacher/student
		teacher = User.objects.create_user("teacherp", "", "123123")
		prof = teacher.profile
		prof.num_licenses=0
		prof.save()
		student_oldname = User.objects.create_user("johnp", "", "default")
		student_oldname.profile.playtime=2000
		student_oldname.profile.save()		
		classroom = Classroom(name="Test Classroom P", school="Test School P", grade="first", num_students=1)
		classroom.save()
		self.classroom_p_id = classroom.id
		ClassroomTeacherRel(user = teacher, classroom=classroom, date=now()).save()
		UserClassroomAssignment(user=student_oldname, classroom=classroom).save()	
		ClassroomActivityBin(classroom=classroom, num_seconds=2000, date=timezone.now()).save()	

		#Not enough licenses trial teacher/student
		teacher = User.objects.create_user("teachernl", "", "123123")
		prof = teacher.profile
		prof.num_licenses = 1
		prof.save()
		classroom = Classroom(name="Test Classroom NL", school="Test School NL", grade="first", num_students=1)
		classroom.save()
		self.classroom_nl_id = classroom.id

		student_oldname = User.objects.create_user("johnnl", "", "default")
		student_oldname.profile.playtime=4000
		student_oldname.profile.save()			
		UserClassroomAssignment(user=student_oldname, classroom=classroom).save()	
		student_oldname = User.objects.create_user("bobnl", "", "default")
		student_oldname.profile.playtime=4000
		student_oldname.profile.save()			
		UserClassroomAssignment(user=student_oldname, classroom=classroom).save()	

		HeatmapPoint(
			user=student_oldname, time=timezone.now(),
			point_x = 0, point_y = 0, point_z = 0, point_type=1,
			level_name="none").save()

		ClassroomTeacherRel(user = teacher, classroom=classroom, date=now()).save()
		UserClassroomAssignment(user=student_oldname, classroom=classroom).save()	
		ClassroomActivityBin(classroom=classroom, num_seconds=14000, date=timezone.now()).save()					

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
		pass

	def json_success(self, r):
		self.assertEqual(r.status_code, 200)
		content = json.loads(r.content)
		self.assertEqual(content['success'], True)
		return content

	def json_failure(self, r):
		self.assertEqual(r.status_code, 200)
		content = json.loads(r.content)
		self.assertEqual(content['success'], False)
		return content		

	def test_register(self):
		c = Client()
		response = c.post("/session/client/register/", {"name":"bob", "classroom":self.classroom_id})
		content = self.json_success(response)
		self.assertEqual(content.has_key("sessionid"), True)
		made_user = User.objects.filter(username=str(self.classroom_id) + "_bob")
		self.assertEqual(made_user.count(), 1)

	def test_login_old(self):
		c = Client()
		response = c.post("/session/client/login/", {"name":"john", "classroom":self.classroom_id})
		content = self.json_success(response)
		self.assertEqual(content.has_key("sessionid"), True)

	def test_login_new(self):
		c = Client()
		c.post("/session/client/register/", {"name":"mary", "classroom":self.classroom_id})
		response = c.post("/session/client/login/", {"name":"mary", "classroom":self.classroom_id})
		content = self.json_success(response)
		self.assertEqual(content.has_key("sessionid"), True)

	def test_register_expired_class(self):
		c = Client()
		response = c.post("/session/client/register/", {"name":"bob", "classroom":self.classroom_x_id})
		content = self.json_success(response)
		made_user = User.objects.filter(username=str(self.classroom_x_id) + "_bob")
		self.assertEqual(made_user.count(), 1)

	def test_login_expired_class(self):
		c = Client()
		response = c.post("/session/client/login/", {"name":"johnx", "classroom":self.classroom_x_id})
		content = self.json_failure(response)
		self.assertEqual(content.has_key("error"), True)
		self.assertIn("expired", content["error"])

	def test_register_partial(self):
		c = Client()
		response = c.post("/session/client/register/", {"name":"bob", "classroom":self.classroom_p_id})
		content = self.json_success(response)
		self.assertEqual(content.has_key("sessionid"), True)
		made_user = User.objects.filter(username=str(self.classroom_p_id) + "_bob")
		self.assertEqual(made_user.count(), 1)

	def test_login_old_partial(self):
		c = Client()
		response = c.post("/session/client/login/", {"name":"johnp", "classroom":self.classroom_p_id})
		content = self.json_success(response)
		self.assertEqual(content.has_key("sessionid"), True)

	def test_register_not_enough_licenses_class(self):
		c = Client()
		response = c.post("/session/client/register/", {"name":"bob", "classroom":self.classroom_nl_id})
		content = self.json_success(response)
		made_user = User.objects.filter(username=str(self.classroom_nl_id) + "_bob")
		self.assertEqual(made_user.count(), 1)

	def test_login_not_enough_licenses_class(self):
		c = Client()
		response = c.post("/session/client/login/", {"name":"johnnl", "classroom":self.classroom_nl_id})
		content = self.json_failure(response)
		self.assertEqual(content.has_key("error"), True)
		self.assertIn("licenses", content["error"])				

	def test_start_session_find_register_login(self):
		# Make a session through the website
		c = Client()
		c.post("/session/start/", {"email":"abc@example.com", "password":"abc123", "classroom_name":"test class"})

		# Find a nearby session
		c = Client()
		response = c.get("/session/client/nearby/")
		content = self.json_success(response)
		self.assertEqual(content["success"], True)
		self.assertEqual(content["sessions"][0]["name"], "test class")
		cid = content["sessions"][0]["id"]

		# Register a user 
		response = c.post("/session/client/register/", {"name":"jenn", "classroom":cid})
		content = self.json_success(response)
		self.assertEqual(content["success"], True)

		#Find a user
		response = c.post("/session/client/names/", {"classroom":cid})
		content = self.json_success(response)
		self.assertEqual(content["success"], True)
		n = content["names"][0]

		#Log in
		response = c.post("/session/client/login/", {"name":n, "classroom":cid})
		content = self.json_success(response)
		self.assertEqual(content["success"], True)
