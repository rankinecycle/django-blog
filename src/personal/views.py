from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from blog.views import get_blog_queryset
from blog.models import BlogPost

BLOG_POSTS_PER_PAGE = 10

# Create your views here.

def home_screen_view(request,*args, **kwargs):
	#print(request.headers)
	# context = {'some_string':'This is the string I am passing to the view (render function in views file.)',
	# 			'my_list': ['first entry','second entry','third entry']
	# 			}
	context ={}

	query = ""
	if request.GET:
		query = request.GET.get('q','') #for empty search
		context['query'] = str(query)

	blog_posts = sorted(get_blog_queryset(query), key =attrgetter('date_updated'), reverse = True)

	# questions = Question.objects.all() # select all objects of class question
	# context['questions'] = questions

	# Pagination
	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

	context['blog_posts'] = blog_posts

	return render(request, "personal/home.html", context)
