from django.contrib.auth.models import User
from django.db import models


def json_default():
    return {'small': None, 'large': None}


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True)
    photo = models.JSONField(default=json_default, null=True)
    subscriptions = models.ManyToManyField(User, related_name='subscriptions')

    def __str__(self):
        return f'{self.user}({self.id})'
