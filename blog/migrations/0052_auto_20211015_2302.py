# Generated by Django 3.1.5 on 2021-10-15 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0051_comment_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replyanswer',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='replyanswer',
            name='author',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='reply_answer',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='ReplyAnswer',
        ),
    ]
