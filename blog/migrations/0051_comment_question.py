# Generated by Django 3.1.5 on 2021-10-15 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0050_auto_20211014_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_comments', to='blog.news'),
        ),
    ]