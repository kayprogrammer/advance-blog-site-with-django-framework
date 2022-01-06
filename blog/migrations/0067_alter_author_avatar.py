# Generated by Django 3.2.8 on 2021-12-28 16:47

import blog.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0066_auto_20211228_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', validators=[blog.validators.avatar_size]),
        ),
    ]