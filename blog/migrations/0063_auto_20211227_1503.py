# Generated by Django 3.2.8 on 2021-12-27 14:03

import blog.validators
import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0062_alter_post_medi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='about',
            name='medi',
        ),
        migrations.RemoveField(
            model_name='news',
            name='medi',
        ),
        migrations.RemoveField(
            model_name='post',
            name='medi',
        ),
        migrations.AddField(
            model_name='about',
            name='image',
            field=models.FileField(blank=True, default='lll.gif/', null=True, upload_to='about_pic'),
        ),
        migrations.AddField(
            model_name='about',
            name='video',
            field=models.FileField(blank=True, null=True, storage=[cloudinary_storage.storage.VideoMediaCloudinaryStorage], upload_to='about_pic/'),
        ),
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.FileField(blank=True, default='lll.gif/', null=True, upload_to='fliers/', validators=[blog.validators.media_size]),
        ),
        migrations.AddField(
            model_name='news',
            name='video',
            field=models.FileField(blank=True, null=True, storage=[cloudinary_storage.storage.VideoMediaCloudinaryStorage], upload_to='fliers/', validators=[blog.validators.media_size]),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, default='lll.gif/', null=True, upload_to='post_pics', validators=[blog.validators.media_size]),
        ),
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, storage=[cloudinary_storage.storage.VideoMediaCloudinaryStorage], upload_to='post_pics/', validators=[blog.validators.media_size]),
        ),
    ]
