from functools import partial

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.forms import widgets
from django.utils.html import conditional_escape, format_html

from mathbreakers.models import *

GRADELEVELS = [
	("k", "Kindergarten"),
	("1", "First Grade"),
	("2", "Second Grade"),
	("3", "Third Grade"),
	("4", "Fourth Grade"),
	("5", "Fifth Grade"),
	("6", "Sixth Grade"),
	("7", "Seventh Grade"),
	("8", "Eighth Grade"),
	("multiple", "Multiple Grade Levels")]

class SignInForm(forms.Form):
	username = forms.CharField(max_length=100, required = True, label = "Username/Email")
	password = forms.CharField(max_length=100, widget=forms.PasswordInput, required = True, label = "Password")

class ChangePasswordForm(forms.Form):
	old_password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True, label="Old Password")
	new_password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True, label="New Password")
	new_password_repeat = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True, label="Repeat New Password")

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super(ChangePasswordForm, self).clean()

		self.request.user.check_password(cleaned_data.get("oldpassword"))

		if cleaned_data.get("new_password") != cleaned_data.get("new_password_repeat"):
			self._errors["new_password_repeat"] = self.error_class(["You must enter the same password."])
		return cleaned_data

class AddClassroomForm(forms.Form):
	school = forms.CharField(min_length=4, max_length = 512, required = True, label="Name of your school*")
	classroom_name = forms.CharField(min_length=4, max_length=256, required=True, label="Name your classroom*")
	grade_level = forms.ChoiceField(GRADELEVELS)

class RedeemPreorderForm(forms.Form):
	why = forms.CharField(required=True, min_length=3, label="Why did you purchase Mathbreakers?")
	recommend = forms.CharField(required=True, min_length=1, label="Would you recommend Mathbreakers to a friend?")
	why_rec = forms.CharField(required=True, min_length=3, label="Why or why not?")
	comments = forms.CharField(required=False, label="Any comments or suggestions?")
	email = forms.EmailField(required = True, label="Email address*")

class ForgotPasswordForm(forms.Form):
	email = forms.EmailField()

class PasswordResetForm(forms.Form):
	new_password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True, label="New Password")
	new_password_repeat = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True, label="Repeat New Password")

class StartLobbyForm(forms.Form):
	email = forms.EmailField(required=True, label="Enter your email address")
	password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True, label="Enter a password")
	classroom_name = forms.CharField(max_length=100, required=True, label="Name your classroom")

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class LobbyLaterForm(forms.Form):
	email = forms.EmailField(required=True)
	day = forms.DateField(widget=DateInput(), label="What day do you plan to use Mathbreakers?")

class WhichClassForm(forms.Form):
	which = forms.ChoiceField(label="Select a class")
	new_class = forms.CharField(max_length=100, required=False, label="Enter new class name")

	def __init__(self, user, *args, **kwargs):
		super(WhichClassForm, self).__init__(*args, **kwargs)
		choices = []
		choices.append((0, "+ New Classroom"))
		for ctr in ClassroomTeacherRel.objects.filter(user=user):
			choices.append((ctr.classroom.id,ctr.classroom.name))
		self.fields['which'].choices = choices

class TeacherPurchaseForm(forms.Form):
	num_students = forms.IntegerField(localize=False, required=True, initial="0", label="Approximately how many students will be playing?")

class HSBCForm(forms.Form):
	code = forms.CharField(max_length=100)

class CodeForm(forms.Form):
	code = forms.CharField(max_length=100)
	email = forms.EmailField(max_length=250)

class SUUserInfoForm(forms.Form):
	username = forms.CharField(max_length=256)

class EducentsCodeForm(forms.Form):
	email = forms.EmailField(required=True, label="Enter your email address")
	password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True, label="Enter a password")
	classroom_name = forms.CharField(max_length=100, required=True, label="Name your classroom")
	