from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager): #creating a custom user manager by modifying create_user and create_super_user from Base user manager class.
	def create_user(self,email,username,password=None):
		if not email: 
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user =  self.model( #function of parent class
			    email=self.normalize_email(email), # converts email to smallcase.
				username = username,
				)
		user.set_password(password)
		user.save(using = self._db)
		return user
	def create_superuser(self,email,username,password):
		user =  self.create_user( #function of parent class
			    email=self.normalize_email(email), # converts email to smallcase.
			    password = password,
				username = username,
				)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser): #creating a custom user
	# These are *required fields
	email					= models.EmailField(verbose_name='email',max_length=60, unique = True)
	username     			= models.CharField(max_length= 30,unique = True)
	date_joined				= models.DateTimeField(verbose_name='date joined',auto_now_add = True)
	last_login				= models.DateTimeField(verbose_name='last login',auto_now = True)
	is_admin				= models.BooleanField(default= False)
	is_active				= models.BooleanField(default= True)
	is_staff				= models.BooleanField(default= False)
	is_superviser			= models.BooleanField(default= False)

	USERNAME_FIELD          = 'email' # equate this variable with whatever you want the user to login with
	REQUIRED_FIELDS			= ['username'] #without which a user can't register

	objects = MyAccountManager() # To tell 'Account' where is the manager

	def __str__(self): #when you print an account object to the template, what should display
		return self.email + ',' + self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin # give permission to change database for admins

	def has_module_perms(self, app_label):
		return True 