# Generated by Django 3.1.5 on 2021-10-05 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_auto_20211005_0116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name_plural': 'News & Info'},
        ),
        migrations.RenameField(
            model_name='news',
            old_name='news',
            new_name='text',
        ),
    ]