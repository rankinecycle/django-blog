from django.db import models

from django.db.models.signals import pre_save,post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
# Create your models here.
 # for defining image upload location

def upload_location(instance,filename):
	# purple is the path for blog/ a image filename
	file_path = 'blog/{author_id}/{title}-{filename}'.format(
			author_id=str(instance.author_id), title=str(instance.title),filename=filename
		)
	return file_path

class BlogPost(models.Model):
	title					= models.CharField(max_length=50, null=False, blank=False) # a blog can't be null or blank
	body					= models.TextField(max_length=5000, null=False, blank=False) #blog body
	image					= models.ImageField(upload_to=upload_location, null= False, blank=False)
	date_published			= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated			= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) 
	# foreign key is same as SQL to join Blogpost with account, but instead of importing it directly here we are saying
	# use the one specified in settings. On deletion, blog only should be deleted not the user.
	slug 					= models.SlugField(blank=True, unique=True)
	#slug means the /(some extra) portion of URL. That should be unique for every blog post.

	def __str__(self):
		return self.title

@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)
#This will clean image from the development env after blog is deleted to save data

def pre_save_blog_post_reciever(sender, instance,*args,**kwargs):
	if not instance.slug: # if no unique slug is created before saving then create it
		instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_reciever, sender=BlogPost) # whenever a saveing attempt is made above function will be called


