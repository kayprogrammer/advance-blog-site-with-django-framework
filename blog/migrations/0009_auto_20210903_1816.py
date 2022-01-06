# Generated by Django 3.1.5 on 2021-09-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210903_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='favourite_quote',
            field=models.CharField(blank=True, help_text='Favourite Quote', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='favourite_scripture',
            field=models.CharField(blank=True, help_text='Favourite Scripture', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='house_address',
            field=models.CharField(blank=True, help_text='Home Address', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='interests',
            field=models.CharField(blank=True, help_text='Interests', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='job_skill',
            field=models.CharField(blank=True, help_text='Job/Skill', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='ministry',
            field=models.CharField(blank=True, help_text='Ministry', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='place_of_worship',
            field=models.CharField(blank=True, help_text='Place of Worship', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='full_name',
            field=models.CharField(help_text='Full Name', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(help_text='Full Name', max_length=200, null=True),
        ),
    ]