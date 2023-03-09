from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from blog.models import BlogPost

 
def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid(): # email, password etc. is valid
			form.save() 
			email = form.cleaned_data.get('email') # To get variable email from input
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email= email, password = raw_password) # will authenticat user
			login(request,account) # will login user
			return redirect('home') #then redirect to home page, named 'home' in urls.py 
		else:
			context['registration_form'] = form # if form isn't valid, then pass it to context to show errors
	else: # it's a get request, user is visiting for the first time, so show him the form
		form = RegistrationForm()
		context['registration_form'] = form 
	return render(request, 'account/register.html', context)

def logout_view(request):
	logout(request)
	return redirect('home')



def login_view(request):
	context = {}
	user = request.user

	if user.is_authenticated:
		return redirect('home') 

	if request.POST: # if data is being sent to server(this computer)
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate( email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")
	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form 
	return render(request, 'account/login.html', context) # return the login page.

def account_view(request):
	if not request.user.is_authenticated:
		return redirect("login")

	context = {}

	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			#To show new email, username after update
			form.initial ={
				"email": request.POST['email'],
				"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = 'Updated'
	else:
		form = AccountUpdateForm(
			initial={ #display the initial email/username before updating
				'email':request.user.email,
				'username':request.user.username,
			}
		)
	context['account_form'] = form 

	blog_posts =BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts

	return render(request, 'account/account.html', context)

def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})

