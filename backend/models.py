# from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _

from backend.validators import *


class User(models.Model):
    email = models.EmailField(unique=True, null=True)
    full_name = models.CharField(max_length=100, validators=[validate_full_name], null=True)
    role = models.CharField(max_length=100, validators=[validate_role], null=True)
    password = models.CharField(_('password'), max_length=128, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE, null=True)
    excel = CloudinaryField(resource_type='auto', null=True)

    def __str__(self):
        return f'{self.user}({self.id})'
