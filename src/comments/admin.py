from django.contrib import admin

# Register your models here.
from comments.models import comments
admin.site.register(comments)