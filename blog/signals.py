from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User, Group
from . models import Author

def users_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='users')
        instance.groups.add(group)

        Author.objects.create(user=instance, full_name=instance.full_name, email=instance.email, phone=instance.phone)
        print('Profile Created!')

post_save.connect(users_profile, sender=settings.AUTH_USER_MODEL)