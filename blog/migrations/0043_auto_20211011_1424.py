# Generated by Django 3.1.5 on 2021-10-11 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0042_auto_20211011_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news_num',
            field=models.IntegerField(default=2021),
        ),
    ]