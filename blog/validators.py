import os
import magic
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _

def validate_is_media(file):
    valid_mime_types = ['video/mp4', 'image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'video/3gp']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.mp4', '.jpg', '.png', '.gif']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')

def validate_is_pic(file):
    valid_mime_types = ['image/jpeg', 'image/jpeg', 'image/png', 'image/gif']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')       


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