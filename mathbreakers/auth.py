from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

def perform_signin(request, username, password):
	#truncated_username = username[:20]
	#user = authenticate(username=truncated_username, password=password)
	username = username[:30]
	user = authenticate(username=username,password=password)
	if user and user.is_active:
		login(request, user)
		request.session.set_expiry(60 * 60 * 24 * 180) # session timeout
		return user
	else:
		return None

def perform_signin_no_password(request, username):
	username = username[:30]
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return None
	if user and user.is_active:
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request, user)
		request.session.set_expiry(60 * 60 * 24 * 180) # session timeout
		return user
	else:
		return None

def perform_logout(request):
	logout(request)
