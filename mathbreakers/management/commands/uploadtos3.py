import time
import datetime
import os

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table
from mathbreakers import mbcopy
from mathbreakers.util import *
from mathbreakers.queries import get_all_teachers_classrooms

def upload_to_bucket(k, local_file_path, prefix = "", compress=True):
	try:
		filename = local_file_path.split("/")[-1]
	except:
		filename = local_file_path

	headers = {}

	if compress:
		temp_zipped_filepath = "temp.gz"
		import gzip
		print "Zipping " + filename
		f = open(local_file_path, "rb")
		gzf = gzip.open(temp_zipped_filepath, "wb")
		gzf.write(f.read())
		gzf.close()
		f.close()

		headers['Content-Encoding'] = "gzip"

		print "Uploading (zipped) " + filename
		upload_local_filepath = temp_zipped_filepath

	else:
		print "Uploading " + local_file_path
		upload_local_filepath = local_file_path

	k.key = prefix + filename
	k.set_contents_from_filename(upload_local_filepath, headers)
	k.set_acl('public-read')
	url = k.generate_url(expires_in=0, query_auth=False)
	print url

class Command(BaseCommand):

	args = 'path of file to upload'
	help = 'Upload a file to s3. Prints the URL.'
	def handle(self, path, prefix="", *args, **options):
		c = S3Connection(settings.AWS_KEY, settings.AWS_SECRET)
		bucket = c.get_bucket("mathbreakers")
		k = Key(bucket)
		try:
			fname = path.split("/")[-1]
		except:
			fname = ""
		if os.path.isdir(path):
			for dirpath, dirnames, filenames in os.walk(path):
				for filename in filenames:
					fullfilename = dirpath + "/" + filename
					inst_prefix = prefix + fname + "/" + dirpath[len(path)+1:]
					if inst_prefix[-1] != "/":
						inst_prefix = inst_prefix + "/"
					inst_prefix = inst_prefix.replace("\\", "/")
					upload_to_bucket(k, fullfilename, inst_prefix)
		else:
			upload_to_bucket(k, path)
