from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField


def json_default():
    return {'small': None, 'large': None}


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE, null=True)
    excel = CloudinaryField(resource_type='auto')

    def __str__(self):
        return f'{self.user}({self.id})'

