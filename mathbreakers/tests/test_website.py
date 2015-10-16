from django.test import TestCase, Client
import subprocess
from mathbreakers.models import *
import requests
import time
import sys
import re
from mathbreakers.settings import DATABASES

class WebsiteTestCase(TestCase):
	def setUp(self):
		PurchaseData(code="mbfull", name="Mathbreakers Full", price=25.00).save()
		PurchaseData(code="teacherpurchase", name="Mathbreakers License", price=3.00).save()

	def check_page_get(self, page):
		c = Client()
		response = c.get(page, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertIn("&copy;", response.content)
		return response.content

	def check_page_post(self, page, args):
		c = Client()
		response = c.post(page, args, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertIn("&copy;", response.content)
		return response.content		

	def test_home(self):
		self.check_page_get("/")

	def test_try(self):
		self.check_page_get("/session/try/")

	def test_post_start(self):
		self.check_page_get("/session/start/")
		args = {
			"email":"morganquirk+test@gmail.com",
			"password":"abc123",
			"classroom_name":"ABC",
		}
		self.check_page_post("/session/start/", args)

	def test_post_later(self):
		self.check_page_get("/session/later/")
		args = {
			"email":"morganquirk+test@gmail.com",
			"day":"01/01/2016",
		}
		self.check_page_post("/session/later/", args)		


	def test_download(self):
		self.check_page_get("/download/")

	def test_buy(self):
		self.check_page_get("/buy/")
