# Generated by Django 3.2.8 on 2021-11-27 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0057_alter_community_standards_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
