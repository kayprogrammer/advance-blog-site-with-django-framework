# Generated by Django 3.1.5 on 2021-09-18 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20210917_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique=True),
        ),
    ]