from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account 

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text='Required.Add a valid email address.')

	class Meta:
		model = Account
		fields = ('email','username','password1','password2') # so that both passwords are same.

class AccountAuthenticationForm(forms.ModelForm):
	password = forms.CharField(label = 'Password', widget = forms.PasswordInput) # A field to enter password
	
	class Meta:
		model = Account 
		fields = ('email','password') # to tell what type of fields is form geeting

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email = email, password = password):
				raise forms.ValidationError("Invalid Login") # non field error, it isn't unique to any one field, handled in login.html

class AccountUpdateForm(forms.ModelForm):
	#To make changes in user database
	class Meta:
		model = Account
		fields = ('email','username')  

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try: #instance is used to get the primary key of the user
				account = Account.objects.exclude(pk = self.instance.pk).get(email=email) #To see if account already exist
			except Account.DoesNotExist:
				return email 
			raise forms.ValidationError('Email "%s" is already in use.' % account.email)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				account = Account.objects.exclude(pk = self.instance.pk).get(username=username) #To see if account already exist
			except Account.DoesNotExist:
				return username 
			raise forms.ValidationError('Username "%s" is already in use.' % account.username)

