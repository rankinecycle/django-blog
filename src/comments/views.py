from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
#FROM BLOGS
from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
#FROM COMMENTS
from comments.models import comments
# and pre_save_comments_reciever is also there
from comments.forms import CreateCommentForm, UpdateCommentForm
#FROM ACCOUNTS
from account.models import Account

# Create your views here.

def create_comment_view(request,slug):
	context = {}

	user =  request.user
	if not user.is_authenticated:
		return redirect('must_authenticate') # redirects to must authenticate.html

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit = False)
		author = Account.objects.filter(email=user.email).first() # filter the user using email
 # author is a required field in forms.py BlogPostForm
		obj.author = author 
		obj.save()
		form = CreateBlogPostForm()
		
	context['form'] = form

	return render(request,"comments/create_comment.html", context)


def edit_comment_view(request, slug):
	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate') 

	comment = get_object_or_404(comments, slug = slug)

	if comment.author != user:
		return HttpResponse('You are not the author of that post.')

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance= comment)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			comment = obj
	form = UpdateCommentForm(
			initial = {
					"comment_text": comment.comment_text,
			}
		)
	context['form'] = form
	return render(request, 'comment/edit_comment.html', context)

def get_comment_queryset(query=None): #Used in homescreenview in views.py - personal
	queryset = []
	queries = query.split(" ") 
	for q in queries:
		posts = comments.objects.filter(
				Q(comment_text__icontains=q)
			).distinct()
# Q lookup imported above, use double underscores
		for post in posts:
			queryset.append(post)

	return list(set(queryset))




