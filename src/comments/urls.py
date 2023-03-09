from django.urls import path
from comments.views import(

		create_comment_view,
		edit_comment_view,
		# comment_view
	)

app_name = 'comments' # use this whenever a main app file like urls.py is made seaprately in some other folder

urlpatterns = [
	path('create/', create_comment_view, name="create"),
	path('<slug>/edit', edit_comment_view, name="edit"),
	#path('<slug>/comments', comment_view, name="comments")			
]