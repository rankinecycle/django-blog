from django.db import models
from django.db import models
from blog.models import BlogPost
from django.db.models.signals import pre_save,post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver

# CODE BY ME

def upload_location(instance,filename):
	# purple is the path for blog/ a image filename
	file_path = 'comments/{blog_id}/{comment_text}'.format(
			blog_id=str(instance.blog_id), title=str(instance.comment_text)
		)
	return file_path

class comments(models.Model):
	blog 							= models.ForeignKey(BlogPost, on_delete = models.CASCADE) #Delete blogpost, comment will get deleted.
	comment_text					= models.TextField(max_length=400, null=False, blank=False)
	date_published					= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated					= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author 							= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) 
	slug 							= models.SlugField(blank=True, unique=True)
	def __str__(self):
		return self.comment_text

def pre_save_comments_reciever(sender, instance,*args,**kwargs):
	if not instance.slug: # if no unique slug is created before saving then create it
		instance.slug = slugify(instance.comment_text[:4])

pre_save.connect(pre_save_comments_reciever, sender=comments) # whenever a saveing attempt is made above function will be called



#END CODE BY ME

