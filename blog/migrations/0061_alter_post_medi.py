# Generated by Django 3.2.8 on 2021-12-27 13:22

import blog.validators
import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0060_auto_20211226_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='medi',
            field=models.FileField(null=True, storage=[cloudinary_storage.storage.VideoMediaCloudinaryStorage, cloudinary_storage.storage.MediaCloudinaryStorage], upload_to='post_pics/', validators=[blog.validators.media_size]),
        ),
    ]
