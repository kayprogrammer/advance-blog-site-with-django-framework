# Generated by Django 3.2.8 on 2022-01-06 20:16

import blog.validators
import ckeditor.fields
import cloudinary_storage.storage
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('full_name', models.CharField(help_text='Full Name', max_length=80, null=True)),
                ('email', models.EmailField(help_text='Email', max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(help_text='Phone', max_length=15, null=True)),
                ('terms_confirmed', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, null=True)),
                ('text', ckeditor.fields.RichTextField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('mission', ckeditor.fields.RichTextField(null=True)),
                ('vision', ckeditor.fields.RichTextField(null=True)),
                ('core_values', ckeditor.fields.RichTextField(null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('support', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('youtube', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('slogan', models.CharField(blank=True, max_length=300, null=True)),
                ('image', models.FileField(blank=True, default='lll.gif/', null=True, upload_to='about_pic')),
                ('video', models.FileField(blank=True, null=True, storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage, upload_to='about_pic/')),
            ],
            options={
                'verbose_name_plural': 'About Us',
            },
        ),
        migrations.CreateModel(
            name='AdminNotifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('text', ckeditor.fields.RichTextField(null=True)),
                ('url', models.URLField(blank=True, max_length=1000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Admin Notifications',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=80, null=True)),
                ('email', models.EmailField(max_length=80, unique=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('bio', ckeditor.fields.RichTextField(blank=True, max_length=3000, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', validators=[blog.validators.avatar_size])),
                ('favourite_quote', models.TextField(blank=True, max_length=1000, null=True)),
                ('favourite_scripture', models.TextField(blank=True, max_length=1000, null=True)),
                ('place_of_worship', models.TextField(blank=True, max_length=1000, null=True)),
                ('house_address', models.TextField(blank=True, max_length=80, null=True)),
                ('job_skill', models.CharField(blank=True, max_length=80, null=True)),
                ('interests', models.TextField(blank=True, max_length=2000, null=True)),
                ('ministry', models.CharField(blank=True, max_length=1000, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=70, null=True)),
                ('comment', models.TextField(max_length=5000)),
                ('date_commented', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Community_Standards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, null=True)),
                ('text', models.TextField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Community Standards',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_num', models.IntegerField(default=2021, unique=True)),
                ('title', models.CharField(max_length=100, null=True)),
                ('text', ckeditor.fields.RichTextField(max_length=10000, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, default='lll.gif/', null=True, upload_to='fliers/', validators=[blog.validators.media_size])),
                ('video', models.FileField(blank=True, null=True, storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage, upload_to='fliers/', validators=[blog.validators.media_size])),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news', to='blog.author')),
            ],
            options={
                'verbose_name_plural': 'News & Info',
            },
        ),
        migrations.CreateModel(
            name='Terms_And_Conditions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, null=True)),
                ('text', ckeditor.fields.RichTextField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Terms & Conditions',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=70, null=True)),
                ('reply', models.TextField(max_length=5000)),
                ('date_replied', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.author')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.comment')),
                ('flagged', models.ManyToManyField(blank=True, related_name='flagged_replies', to='blog.Author')),
            ],
            options={
                'verbose_name_plural': 'Replies',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('text', models.TextField(null=True)),
                ('slug', models.SlugField(blank=True, max_length=250)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.author')),
                ('category', models.ManyToManyField(to='blog.Category')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('body', ckeditor.fields.RichTextField(null=True)),
                ('slug', models.SlugField(blank=True, max_length=250)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, default='lll.gif/', null=True, upload_to='post_pics/', validators=[blog.validators.media_size])),
                ('video', models.FileField(blank=True, null=True, storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage, upload_to='post_pics/', validators=[blog.validators.media_size])),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.author')),
                ('category', models.ManyToManyField(related_name='posts', to='blog.Category')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.IntegerField()),
                ('news_num', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('text', models.TextField(blank=True, max_length=10000, null=True)),
                ('from_visitor', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author_has_seen', models.BooleanField(default=False)),
                ('admin_notifications', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.adminnotifications')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.post')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.comment')),
                ('from_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_from', to='blog.author')),
                ('news', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.news')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.question')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.reply')),
                ('to_author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_to', to='blog.author')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('message', models.TextField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.author')),
            ],
            options={
                'verbose_name_plural': 'Message',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.author'),
        ),
        migrations.AddField(
            model_name='comment',
            name='flagged',
            field=models.ManyToManyField(blank=True, related_name='flagged_comments', to='blog.Author'),
        ),
        migrations.AddField(
            model_name='comment',
            name='news',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news_comments', to='blog.news'),
        ),
        migrations.AddField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_comments', to='blog.question'),
        ),
        migrations.AddField(
            model_name='author',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.title'),
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
