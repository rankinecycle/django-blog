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
from comments.views import get_comment_queryset
#FROM ACCOUNTS
from account.models import Account

from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



def create_blog_view(request): 
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

	return render(request,"blog/create_blog.html", context)

def detail_blog_view(request, slug):
	context = {}
	blog_post = get_object_or_404(BlogPost, slug = slug) # import from django.shortcuts
	context['blog_post'] = blog_post

	query = ""
	if request.GET:
		query = request.GET.get('q','') #for empty search
		context['comment_text'] = str(query)
	comment_text = sorted(get_comment_queryset(query), key =attrgetter('date_updated'), reverse = True)

	context['comment_text'] = comment_text

	return render(request, 'blog/detail_blog.html', context)

def edit_blog_view(request, slug):
	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate') 

	blog_post = get_object_or_404(BlogPost, slug = slug)

	if blog_post.author != user:
		return HttpResponse('You are not the author of that post.')

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance= blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj
	form = UpdateBlogPostForm(
			initial = {
					"title": blog_post.title,
					"body": blog_post.body,
					"image": blog_post.image,
			}
		)
	context['form'] = form
	return render(request, 'blog/edit_blog.html', context)

def get_blog_queryset(query=None): #Used in homescreenview in views.py - personal
	queryset = []
	queries = query.split(" ") 
	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) |
				Q(body__icontains=q)
			).distinct()
# Q lookup imported above, use double underscores
		for post in posts:
			queryset.append(post)

	return list(set(queryset))

