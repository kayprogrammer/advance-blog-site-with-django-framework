# Generated by Django 3.1.5 on 2021-10-11 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0048_auto_20211011_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='about',
            name='slogan',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
