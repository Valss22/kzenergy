from django.db import models
from cloudinary.models import CloudinaryField
from backend.validators import *
import datetime


class User(models.Model):
    email = models.EmailField(null=True)
    fullName = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=128, null=True)

    def __str__(self):
        return f'{self.fullName}({self.email})'


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE, null=True)
    excel = CloudinaryField(resource_type='auto', null=True)

    def __str__(self):
        return f'{self.user}({self.id})'


class GasCompositionCompressor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=datetime.datetime.now(), null=True)


class Compressor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=datetime.datetime.now(), null=True)
    gasConsumptionVolume = models.IntegerField(null=True)
    volumeOfInjectedGas = models.IntegerField(null=True)
    workingHours = models.IntegerField(null=True)
    gasComposition = models.JSONField(null=True)
    wasteGases = models.IntegerField(null=True)
