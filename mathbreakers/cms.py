import json

import requests
from requests.auth import HTTPBasicAuth


RIQ_API_KEY=""
RIQ_API_SECRET=""

def add_contact(email, name, school, phone=None):
	obj = {
		"properties":
		{
			"name":[{"value":name}],
			"email":[{"value":email}],
			"school":[{"value":school}],
			"phone":[{"value":phone}],
		}
	}
	relateiq_post("contacts", obj)

def relateiq_post(endpoint, payload):
	headers = {
		"Content-Type": "application-json",
		"Accept": "application-json",
	}

	requests.post("https://api.relateiq.com/v2/" + endpoint,
		auth=HTTPBasicAuth(RIQ_API_KEY, RIQ_API_SECRET),
		headers=headers,
		data=json.dumps(payload))