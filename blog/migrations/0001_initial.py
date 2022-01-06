# Generated by Django 3.1.5 on 2021-07-28 03:15

import autoslug.fields
import blog.validators
import ckeditor.fields
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
                ('full_name', models.CharField(help_text='Full Name', max_length=40, null=True)),
                ('email', models.EmailField(help_text='Email', max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(help_text='Phone', max_length=15, null=True)),
                ('terms_confirmed', models.BooleanField(default=True)),
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
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Full Name', max_length=20, null=True)),
                ('email', models.EmailField(help_text='Email', max_length=100, unique=True)),
                ('phone', models.CharField(help_text='Phone', max_length=15, null=True)),
                ('bio', ckeditor.fields.RichTextField(blank=True, max_length=1000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='Date added')),
                ('avatar', models.ImageField(blank=True, default='pro.png', null=True, upload_to='avatars')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
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
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
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
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.author')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.comment')),
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
                ('text', ckeditor.fields.RichTextField(null=True)),
                ('slug', autoslug.fields.AutoSlugField(blank=True, editable=False, max_length=250, populate_from=models.CharField(max_length=100, null=True), unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, default='lll.gif', null=True, upload_to='media/')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.author')),
                ('category', models.ManyToManyField(to='blog.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('body', ckeditor.fields.RichTextField(null=True)),
                ('slug', models.SlugField(blank=True, max_length=250)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('medi', models.FileField(null=True, upload_to='media', validators=[blog.validators.validate_is_media])),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.author')),
                ('category', models.ManyToManyField(to='blog.Category')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('news', ckeditor.fields.RichTextField(max_length=10000, null=True)),
                ('slug', autoslug.fields.AutoSlugField(blank=True, editable=False, max_length=250, populate_from=models.CharField(max_length=100, null=True), unique_with=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('media', models.FileField(blank=True, default='lll.gif', null=True, upload_to='media/', validators=[blog.validators.validate_is_media])),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.author')),
            ],
            options={
                'verbose_name_plural': 'News',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.author'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('answer', models.TextField(max_length=3000, null=True)),
                ('date_answered', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, default='lll.gif', null=True, upload_to='media/')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.author')),
            ],
        ),
    ]
