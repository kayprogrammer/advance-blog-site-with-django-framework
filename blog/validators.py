import os
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _

full_regex_pattern = RegexValidator(regex=r'^[a-zA-Z]+\s[a-zA-Z]*$', message='Please input only two names without digits or special characters.',)

phone_regex_pattern =  RegexValidator(regex=r'^\+[0-9]*$', message="Please include your country code and digits only (start with a '+' sign)")

def emailValidator(value):
    if len(value) < 6:
        raise ValidationError(_('\'%(value)s\' is too short. (Use 6 chars or more)'), params={'value':value},)
    else:
        return value

def fullnameValidator(value):
    if len(value) < 6:
        raise ValidationError(_('\'%(value)s\' is too short. (Use 6 chars or more)'), params={'value':value},)
    else:
        return value

def file_size(value): # add this to some file where you can import it from
    limit = 3 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 3 MiB.')

def media_size(value): # add this to some file where you can import it from
    limit = 15 * 1024 * 1024

    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 7 MiB.')        

def avatar_size(value):
    limit = 2 * 1024 * 1024
    if value.size != None:
        if value.size > limit:
            raise ValidationError('File too large. Size should not exceed 2 MiB.')
