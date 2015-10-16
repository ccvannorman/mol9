from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
import time
import datetime
from mathbreakers import mbcopy
from mathbreakers.util import *
from django.utils import timezone

class Command(BaseCommand):

	args = ''
	help = 'Crontab runs this every hour. It checks if there are any saved emails in RobotToSendEmail and if the date matches, it sends the email and removes the row from RobotToSendEmail'
	def handle(self, *args, **options):
		message = ""
		subject = ""
		num_emailed = 0
		num_skipped = 0
		date = time.strptime(str(day), "%Y-%m-%d")
		#mt = datetime.fromtimestamp(mktime(struct))
		mt = datetime.datetime(*date[:6])
		# nicedate = time.strftime("%A, %B %d",time.gmtime(mt)) #time.gmtime(date))
		subject = TEACHER_SCHEDULED_A_PLAY_SESSION[0]
		message = TEACHER_SCHEDULED_A_PLAY_SESSION[1].format("nicedate")
		# struct = time.strptime(date, "%m/%d/%Y %H:%M:%S")
		# dt = datetime.datetime.fromtimestamp(time.mktime(struct))
	
		rtse = RobotToSendEmail(email=em, title=subject, content=message, time=date)
		rtse.save()
		tl = TryLater(
			email = em,
			schedule_support=True,
			schedule_play = day,
			ip = get_ip(request),
			time = timezone.now()
		)
		for item in TryLater.objects.all():
			print " " + item.email
			nicedate = item.date.strftime("%A, %B %d")
			dif = item.date - timezone.now()
			print str(item.date - timezone.now())
			if dif < 1:
				subject = item.title
				message = item.content
				if RobotSentEmail.objects.filter(title=subject,email=item.email).exists():
					print 'SKIP: .. robot already sent email to ' + item["user"].email + ' with subject ' + s + ", skipping"
					num_skipped += 1
					continue
				else:
					print "SENT: .. " + item.email + " with date " + item.date
					num_emailed += 1
					time.sleep(1)
					send_mail_sync(subject,message,'charlie@mathbreakers.com',[item.email])
					item.delete()
