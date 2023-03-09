from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #Helper class to make admin screens
from account.models import Account


class AccountAdmin(UserAdmin):
	list_display = ('email','username','date_joined','last_login','is_admin','is_staff') #Do display as columns in admin screen
	search_fields = ('email','username',) #will allow to search by username and email
	readonly_fields = ('date_joined','last_login') #as they are auto updated 

	filter_horizontal = () #Don't want these options but they should be present
	list_filter = ()
	fieldsets = ()

admin.site.register(Account, AccountAdmin)

# Register your models here.
