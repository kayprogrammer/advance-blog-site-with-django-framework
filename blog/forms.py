from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django_bleach.forms import BleachField

from ckeditor.widgets import CKEditorWidget
from . models import * 
from . validators import *

class PostForm(ModelForm):
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your article title... '}))
	body = forms.CharField(widget=CKEditorWidget(config_name='awesome_ckeditor', attrs={'class':'form-control'}))
	category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple())
	image = forms.ImageField(required=False, validators=[media_size], widget=forms.FileInput(attrs={'class':'input-file', 'type':'file', 'id':'file', 'size':5, 'accept': ['image/jpeg', 'image/png', 'image/gif', 'image/bmp'] }))
	video = forms.FileField(required=False, validators=[media_size], widget=forms.FileInput(attrs={'class':'input-file', 'type':'file', 'id':'file2', 'size':5, 'accept': ['image/jpeg', 'image/png', 'image/gif', 'image/bmp'] }))

	def clean_category(self):
		category = self.cleaned_data['category']
		if len(category) > 3:
			raise forms.ValidationError('Two categories max.')
		return category

	class Meta:
		model = Post
		fields = '__all__'
		exclude = ['slug', 'author', 'date_created']


class NewsForm(ModelForm):
	news_num = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'It has to be unique... '}))
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your article title... '}))
	text = forms.CharField(widget=forms.Textarea( attrs={'class':'form-control n-text' }))
	image = forms.ImageField(required=False, validators=[media_size], widget=forms.FileInput(attrs={'class':'input-file', 'type':'file', 'id':'file', 'size':5, 'accept': ['image/jpeg', 'image/png', 'image/gif', 'image/bmp'] }))
	video = forms.FileField(required=False, validators=[media_size], widget=forms.FileInput(attrs={'class':'input-file', 'type':'file', 'id':'file2', 'size':5, 'accept': ['video/mp4', 'video/3gp'] }))

	class Meta:
		model = News
		fields = '__all__'
		exclude = ['author', 'date_created', 'slug']

class QuestionForm(ModelForm):
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your article title... '}))
	text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control textarea--style-6', 'placeholder':'Type in your question...'}))
	category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple())
	
	def clean_category(self):
		category = self.cleaned_data['category']
		if len(category) > 2:
			raise forms.ValidationError('Two categories max.')
		return category

	class Meta:
		model = Question
		fields = ['title', 'text', 'category']

class CommentForm(ModelForm):

	name = forms.CharField(max_length=40, validators=[full_regex_pattern, fullnameValidator], widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name *', 'type':'name'}))
	email = forms.CharField(max_length=100, validators=[emailValidator], widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email *', 'type':'email'}))
	comment = forms.CharField(max_length=10000, required = True, widget=forms.Textarea(attrs={'class':'form-control comm', 'placeholder':'Comment', 'rows':'60', 'type':'text'}))
	class Meta: 
		model = Comment
		fields = '__all__'
		exclude = ['article', 'news', 'question']

	def __init__(self, user, *args, **kwargs):
		super(CommentForm, self).__init__(*args, **kwargs)
		if user.is_authenticated:
			self.fields['name'].required = False
			self.fields['email'].required = False
		else:
			self.fields['name'].required = True
			self.fields['email'].required = True

class ReplyForm(ModelForm):

	name = forms.CharField(max_length=40, validators=[full_regex_pattern], widget=forms.TextInput(attrs={'class':'form-control replll', 'placeholder':'Full Name *', 'type':'name'}))
	email = forms.CharField(max_length=100, validators=[emailValidator], widget=forms.EmailInput(attrs={'class':'form-control replll', 'placeholder':'Email *', 'type':'email'}))
	reply = forms.CharField(max_length=10000, required = True, widget=forms.Textarea(attrs={'class':'form-control repp', 'placeholder':'Reply', 'rows':'60', 'type':'text'}))
	class Meta: 
		model = Reply
		fields = '__all__'
		exclude = ['comment']

	def __init__(self, user, *args, **kwargs):
		super(ReplyForm, self).__init__(*args, **kwargs)
		if user.is_authenticated:
			self.fields['name'].required = False
			self.fields['email'].required = False
		else:
			self.fields['name'].required = True
			self.fields['email'].required = True		

class RegisterForm(UserCreationForm):

	full_name = forms.CharField(max_length=40, validators=[full_regex_pattern], widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Full Name'}))
	email = forms.CharField(max_length=100, validators=[emailValidator], widget=forms.EmailInput(attrs={'class':'input', 'placeholder':'Email Address'}))
	phone = forms.CharField(max_length=15, validators=[phone_regex_pattern], widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Phone Number'}))
	password1 = forms.CharField(max_length=25, widget=forms.PasswordInput(attrs={'class':'input', 'placeholder':'Password'}))
	password2 = forms.CharField(max_length=25, widget=forms.PasswordInput(attrs={'class':'input', 'placeholder':'Confirm Password'}))
	terms_confirmed = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class':'checkbox',}))

	class Meta:
		model = User
		fields = ['full_name', 'email', 'phone', 'password1', 'password2']

	def clean_password2(self):
		super(RegisterForm, self).clean()

		# This method will set the `cleaned_data` attribute

		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if not password1 == password2:
			raise forms.ValidationError('Password Mismatch')
		if len(password1) < 8:
			raise forms.ValidationError('Password is too short')
		return password2		

	def clean_full_name(self):
		full_name = self.cleaned_data['full_name']
		if len(full_name) < 6:
			raise forms.ValidationError(_('\'%(full_name)s\' is too short. (Use 6 chars or more)'), params={'full_name':full_name})	
		return full_name	

class ProfileForm(ModelForm):


	title = forms.ModelChoiceField(queryset=Title.objects.all())
	full_name = forms.CharField(max_length=80, validators=[full_regex_pattern, fullnameValidator], widget=forms.TextInput())
	phone = forms.CharField(max_length=15, validators=[phone_regex_pattern], widget=forms.TextInput())
	bio = BleachField(required = False, max_length=3000, widget= forms.Textarea(attrs={'class':'input--style-6', 'placeholder':'Write something about yourself...'}))
	house_address = forms.CharField(required = False, max_length=80, widget=forms.TextInput())
	place_of_worship = forms.CharField(required = False, max_length=1000, widget=forms.Textarea())
	job_skill = forms.CharField(required = False, max_length=80, widget=forms.TextInput())
	ministry = forms.CharField(required = False, max_length=1000, widget=forms.Textarea(attrs={'placeholder':'What is God\'s call in your life...'}))
	interests = forms.CharField(required = False, max_length=2000, widget=forms.Textarea())
	birthday = forms.DateField(required = False, widget=forms.DateInput(attrs={'type':'date'}))
	favourite_scripture = forms.CharField(required = False, max_length=1000, widget=forms.Textarea())
	favourite_quote = forms.CharField(required = False, max_length=1000, widget=forms.Textarea())
	avatar = forms.ImageField(required=False, validators=[avatar_size], widget=forms.FileInput(attrs={ 'type':'file', 'id':'file', 'size':5, 'class':'input-file' }))

	class Meta:
		model = Author
		fields = '__all__'
		exclude = ['user', 'email', 'date_created', 'slug']

	def __init__(self, user, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		if user.is_staff:
			self.fields['bio'].widget= CKEditorWidget(config_name='awesome_ckeditor', attrs={'class':'input--style-6', 'placeholder':'Write something about yourself...'})	

class PostSearchForm(forms.Form):
    q = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control tm-search-input', 'name':'query', 'type':'text', 'aria-label':'Search', 'placeholder':'Search...'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control menudd tm-search-input'})
        self.fields['q'].widget.attrs.update(
            {'data-toggle': 'dropdown'})

class ContactForm(ModelForm):
  name = forms.CharField(max_length=80, validators=[full_regex_pattern, fullnameValidator], widget=forms.TextInput(attrs={'class':'form-control rounded-pill mb-1', 'placeholder': 'Enter your full name...'}))
  email = forms.CharField(max_length=100, validators=[emailValidator], widget=forms.EmailInput(attrs={'class':'form-control rounded-pill mb-1', 'placeholder':'Enter your email address...'}))
  message = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'form-control mb-2', 'id':'contact', 'placeholder':'Tell us something...'}))
  
  class Meta: 
    model = Contact
    fields = '__all__'
    exclude = ['author']

  def __init__(self, user, *args, **kwargs):
    super(ContactForm, self).__init__(*args, **kwargs)
    if user.is_authenticated:
    	self.fields['name'].required = False
    	self.fields['email'].required = False
    else:
    	self.fields['name'].required = True
    	self.fields['email'].required = True