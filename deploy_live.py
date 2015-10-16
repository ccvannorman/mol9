import os
import sys
import subprocess

os.system("rm lite_test.db")

# py = "C:\\Python27\\python.exe"
# py = "/usr/bin/python"
py = sys.executable

status = os.popen("git status").read()
if "On branch master" not in status:
	print "You should be on the master branch for this."
	quit()

if "working directory clean" not in status:
	print "You should commit your changes."
	quit()

status = os.popen("git pull").read()
if "Already up-to-date." not in status:
	print "Make sure the pull worked and deploy again"

test_results = subprocess.check_output([py, "manage.py", "test", "mathbreakers"])

if "FAILED" in test_results:
	print "FAILED"
	quit()


# Set live's head to be ours
os.system("git checkout live")
os.system("git pull origin live")
os.system("git checkout master")
os.system("git merge -s ours live")
os.system("git checkout live")
# Then give the changes to master
os.system("git merge master")

print "Pushing to live."
os.system("git push origin live")

print "Alright we're all set. Going back to master branch."
os.system("git checkout master")

print "You probably want to git push now! Not doing it automatically just in case."