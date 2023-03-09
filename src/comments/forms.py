from django import forms
from blog.models import BlogPost
from comments.models import comments
from account.models import Account

class CreateCommentForm(forms.ModelForm):

	class Meta:
		model = comments
		fields = ['comment_text'] #refer to models

class UpdateCommentForm(forms.ModelForm):
	class Meta:
		model = comments
		fields = ['comment_text']

	def save(self, commit=True):
		comment = self.instance #this should be the comment object having dates,authours,etc.
		comment.comment_text = self.cleaned_data['comment_text'] 

		if commit:
			comment.save()

		return comment