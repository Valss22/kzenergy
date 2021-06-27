from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE, null=True)
    excel = CloudinaryField(resource_type='auto', null=True)

    def __str__(self):
        return f'{self.user}({self.id})'

