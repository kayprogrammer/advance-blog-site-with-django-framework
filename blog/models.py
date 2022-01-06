from django.db import models
from django.db.models.fields import *
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import RawMediaCloudinaryStorage, VideoMediaCloudinaryStorage, MediaCloudinaryStorage 

from ckeditor.fields import RichTextField

from autoslug import AutoSlugField
from . utils import unique_slug_generator, unique_slug_generator2, unique_slug_generator3
from . validators import avatar_size, media_size
from mimetypes import guess_type
import mimetypes
import os
#import magic
import math
from os.path import splitext
from django.dispatch import receiver

# User managers and models

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=80, help_text='Full Name', null=True)
    email = models.EmailField(_('email address'), unique = True, help_text='Email')
    USERNAME_FIELD = 'email'
    phone = models.CharField(max_length=15, help_text='Phone', null=True )
    terms_confirmed = models.BooleanField(null=False, blank=False, default=True)
    is_verified = models.BooleanField(default=False)
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return str(self.full_name)

class Title(models.Model):
    title = models.CharField(max_length=5, null=True)

    def __str__(self):
        return str(self.title)

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=False, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, null=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=80, null=True)
    email = models.EmailField(max_length=80, unique=True)
    phone = models.CharField(max_length=15, null=True)
    bio = RichTextField(config_name='awesome_ckeditor', max_length=3000, null=True, blank=True)
    slug = models.SlugField(max_length=250, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(default='pro_lrubcc.png', upload_to='avatars/', null=True, blank=True, validators=[avatar_size])
    favourite_quote = models.TextField(max_length=1000, null=True, blank=True)
    favourite_scripture = models.TextField(max_length=1000, null=True, blank=True)
    place_of_worship = models.TextField(max_length=1000, null=True, blank=True)
    house_address = models.TextField(max_length=80,null=True, blank=True)
    job_skill = models.CharField(max_length=80, null=True, blank=True)   
    interests = models.TextField(max_length=2000, null=True, blank=True)
    ministry = models.CharField(max_length=1000, null=True, blank=True)   
    birthday = models.DateField(null=True, blank=True)

    def whenmodified(self):
        now = timezone.now()
        
        diff = now - self.modified

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds < 60:
                return "Just now"
            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def __str__(self):
        return str(self.full_name)

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.slug)])

    @property
    def avatarURL(self):
        try:
            url = self.avatar.url
        except:
            url = "/media/pro.png"
        return url
'''
@receiver(pre_save, sender=Author)
def delete_old_file(sender, instance, **kwargs):
    # on creation, signal callback won't be triggered 
    if instance._state.adding and not instance.pk:
        return False
    
    try:
        old_file = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False
    
    # comparing the new file with the old one
    file = instance.avatar
    if not old_file == file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
'''

def slug_generator5(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator3(instance)

pre_save.connect(slug_generator5, sender=Author)

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=250, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.name)

    @classmethod
    def query_choice(cls, slug, self):
        return cls.objects.get(slug = self.slug)

    '''
    @classmethod
    def get_posts(self):
        articles = [self.posts]
        return articles
    '''
def slug_generator2(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator2(instance)

pre_save.connect(slug_generator2, sender=Category)        

class Post(models.Model):
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100, null=True)
    body = RichTextField(config_name='awesome_ckeditor', null=True)
    slug = models.SlugField(max_length=250, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, related_name="posts")
    image = models.ImageField(default='jes_vcjwrw.jpg', upload_to='post_pics/', null=True, blank=True, validators=[media_size])
    video = models.FileField(upload_to='post_pics/', null=True, blank=True, validators=[media_size], storage=VideoMediaCloudinaryStorage)

    class Meta:
        ordering = ['-date_created']    

    def get_comment_count(self):
        com_ammount = self.comments.all().count() 
        if com_ammount == 1:
            return str(com_ammount) + ' comment'
        elif com_ammount < 1:
            return 'No comments'
        else:
            return str(com_ammount) + ' comments'       

    @property  
    def get_absolute_url(self):
        return reverse('post_detail', args=[int(self.id), str(self.slug)])        

    def whenpublished(self):
        now = timezone.now()
        
        diff = now - self.date_created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds < 60:
                return "Just now"
            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def whenmodified(self):
        now = timezone.now()
        
        diff = now - self.modified

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds < 60:
                return "Just now"
            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def __str__(self):
        return str(self.title)
'''
@receiver(pre_save, sender=Post)
def delete_old_file(sender, instance, **kwargs):
    # on creation, signal callback won't be triggered 
    if instance._state.adding and not instance.pk:
        return False
    
    try:
        old_file = sender.objects.get(pk=instance.pk).medi
    except sender.DoesNotExist:
        return False
    
    # comparing the new file with the old one
    file = instance.medi
    if not old_file == file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
'''
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)

class Question(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100, null=True)
    text = models.TextField(null=True)
    slug = models.SlugField(max_length=250, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category)

    class Meta:
        ordering = ['-date_created']

    def whenpublished(self):
        now = timezone.now()
        
        diff = now - self.date_created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds < 60:
                return "Just now"
            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def whenmodified(self):
        now = timezone.now()
        
        diff = now - self.modified

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds < 60:
                return "Just now"
            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('question_detail', args=[int(self.id), str(self.slug)])        

def slug_generator3(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator3, sender=Question)

class News(models.Model):
    author = models.ForeignKey(Author, related_name = "news", on_delete=models.SET_NULL, null=True, blank=True)
    news_num = models.IntegerField(default=2021, unique=True, blank=False, null=False)
    title = models.CharField(max_length=100, null=True)
    text = RichTextField(config_name="awesome_ckeditor", max_length=10000, null=True)
    slug = models.SlugField(max_length=250, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='lll.gif/', upload_to='fliers/', null=True, blank=True, validators=[media_size])
    video = models.FileField(upload_to='fliers/', null=True, blank=True, validators=[media_size], storage=VideoMediaCloudinaryStorage)

    '''
    @classmethod
    def notify_all(klass, title, text):
        new_notices = list()
        for a in Author.objects.all():
            new_notices.append(klass(to_author=a, title=title, text=text))
            klass.objects.bulk_create(new_notices)
    '''

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.slug)])

    '''
    def media_type_html(self):
        """
        guess_type returns a tuple like (type, encoding) and we want to access
        the type of media file in first index of tuple
        """
        type_tuple = guess_type(self.mediaURL, strict=True)
        if (type_tuple[0]).__contains__("image"):
            return "image"
        elif (type_tuple[0]).__contains__("video"):
            return "video"
    '''
    def whenpublished(self):
        now = timezone.now()
        
        diff = now - self.date_created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds < 60:
                return "Just now"
            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def whenmodified(self):
        now = timezone.now()
        
        diff = now - self.modified

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds < 60:
                return "Just now"
            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


    class Meta:
        verbose_name_plural = 'News & Info' 

def slug_generator4(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator4, sender=News)

class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    article = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_comments', null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_comments', null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=70, null=True, blank=True)
    flagged = models.ManyToManyField(Author, blank=True, related_name='flagged_comments')
    comment = models.TextField(max_length=5000)
    date_commented = models.DateTimeField(auto_now_add=True)

    def replys(self):
        rep = self.replies.all()
        return rep

    def whenpublished(self):
        now = timezone.now()
        
        diff = now - self.date_commented

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds < 60:
                return "Just now"
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " min ago"
            
            else:
                return str(minutes) + " mins ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hr ago"

            else:
                return str(hours) + " hrs ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " mth ago"

            else:
                return str(months) + " mths ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " yr ago"

            else:
                return str(years) + " yrs ago"

    def __str__(self):
        return ' {}: {}'.format(self.name or self.author, self.comment)

    

class Reply(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=70, null=True, blank=True)
    flagged = models.ManyToManyField(Author, blank=True, related_name='flagged_replies')
    reply = models.TextField(max_length=5000)
    date_replied = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Replies'

    def whenpublished(self):
        now = timezone.now()
        
        diff = now - self.date_replied

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds < 60:
                return "Just now"
            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " min ago"
            
            else:
                return str(minutes) + " mins ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hr ago"

            else:
                return str(hours) + " hrs ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " mth ago"

            else:
                return str(months) + " mths ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " yr ago"

            else:
                return str(years) + " yrs ago"

    def __str__(self):
        return ' {}: {}'.format(self.name or self.author, self.reply)

class AdminNotifications(models.Model):
    title = models.CharField(max_length=1000, null=True, blank=True)
    text = RichTextField(config_name='awesome_ckeditor', null=True)
    url = models.URLField(max_length=1000, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = 'Admin Notifications'

class Notification(models.Model):
	# 1 = Comment, 2 = Reply, 3= register, 4 = news, 5 = warning, 6 = flagged_comment, 7 = flagged_reply
    notification_type = models.IntegerField()
    news_num = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    text = models.TextField(max_length=10000, null=True, blank=True)
    to_author = models.ForeignKey(Author, related_name='notification_to', on_delete=models.CASCADE, null=True, blank=True)
    from_author = models.ForeignKey(Author, related_name='notification_from', on_delete=models.CASCADE, null=True)
    from_visitor = models.CharField(max_length=100, null=True, blank=True)
    article = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    reply = models.ForeignKey('Reply', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    author_has_seen = models.BooleanField(default=False)
    admin_notifications = models.ForeignKey(AdminNotifications, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def all_authors(self):
        authors = self.authors_set.all()
        return authors

    def __str__(self):
        return ' {}: {}: {}: {}'.format(self.id, self.notification_type, self.to_author, self.title)

class Terms_And_Conditions(models.Model):
    title = models.CharField(max_length=1000, null=True)
    text = RichTextField(config_name='awesome_ckeditor', null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = 'Terms & Conditions'

class Community_Standards(models.Model):
    title = models.CharField(max_length=1000, null=True)
    text = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = 'Community Standards'

class About(models.Model):
    title = models.CharField(max_length=1000, null=True)
    text = RichTextField(config_name='awesome_ckeditor', null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    mission = RichTextField(config_name='awesome_ckeditor', null=True)
    vision = RichTextField(config_name='awesome_ckeditor', null=True)
    core_values = RichTextField(config_name='awesome_ckeditor', null=True)
    address = models.TextField(null=True, blank=True)
    support = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    slogan = models.CharField(max_length=300, null=True, blank=True)
    image = models.FileField(default='lll.gif/', upload_to='about_pic', null=True, blank=True)
    video = models.FileField(upload_to='about_pic/', null=True, blank=True, storage=VideoMediaCloudinaryStorage)


    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = 'About Us'       
            
    @property
    def mediaURL(self):
        try:
            url = self.medi.url
        except:
            url = "/media/lll.gif"
        return url
    '''
    def media_type_html(self):
        """
        guess_type returns a tuple like (type, encoding) and we want to access
        the type of media file in first index of tuple
        """
        type_tuple = guess_type(self.mediaURL, strict=True)
        if (type_tuple[0]).__contains__("image"):
            return "image"
        elif (type_tuple[0]).__contains__("video"):
            return "video"
    '''
class Contact(models.Model):
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length = 200, null=True, blank=True)
    email = models.EmailField(max_length = 100, null=True, blank=True) 
    message = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author or self.name)

    class Meta:
        verbose_name_plural = 'Message'
                    
