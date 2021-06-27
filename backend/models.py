from django.contrib.auth.models import User
from django.db import models


def json_default():
    return {'small': None, 'large': None}


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    excel = models.FileField(null=True)

    def __str__(self):
        return f'{self.user}({self.id})'
