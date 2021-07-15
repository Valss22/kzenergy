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
        return f'{self.fullName}'


# class UserRefreshToken(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     refresh = models.TextField(null=True)
#
#     def __str__(self):
#         return f'{self.user}({self.id})'


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE, null=True)
    excel = CloudinaryField(resource_type='auto', null=True)

    def __str__(self):
        return f'{self.user}({self.id})'


class Gas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.CharField(default=None, max_length=50, null=True)
    gasName = models.CharField(max_length=50, null=True)
    nitrogen = models.FloatField(help_text='% масс N', null=True)
    sulfur = models.FloatField(help_text='% масс S', null=True)
    carbon = models.FloatField(help_text='% масс C', null=True)
    density = models.FloatField(help_text='плотность газа', null=True)
    CO2EmissionFactor = models.FloatField(help_text='тСО2/ТДж', null=True)
    CH4SpecificFactor = models.IntegerField(help_text='кг/ТДж', null=True)
    N2OSpecificFactor = models.IntegerField(help_text='кг/ТДж', null=True)
    LowerHeatCombustion = models.FloatField(help_text='ТГ, ГДж/т', null=True)

    def __str__(self):
        return f'{self.gasName}({self.id})'


class Compressor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.CharField(default=None, max_length=50, null=True)
    gasConsumptionVolume = models.FloatField(help_text='тыс. м3', null=True)
    volumeOfInjectedGas = models.FloatField(help_text='тыс. м3', null=True)
    workingHours = models.FloatField(help_text='часы', null=True)
    gasComposition = models.OneToOneField(Gas, help_text='г/с', on_delete=models.CASCADE, null=True)


class PowerPlant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.CharField(default=None, max_length=50, null=True)
    gasConsumptionVolume = models.FloatField(help_text='тыс. м3', null=True)
    generatedElectricity = models.FloatField(help_text='МВт*ч', null=True)
    workingHours = models.FloatField(help_text='часы', null=True)
    gasComposition = models.OneToOneField(Gas, help_text='г/с', on_delete=models.CASCADE, null=True)


class Boiler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.CharField(default=None, max_length=50, null=True)
    gasConsumptionVolume = models.FloatField(help_text='тыс. м3', null=True)
    steamVolume = models.FloatField(help_text='т', null=True)
    workingHours = models.FloatField(help_text='часы', null=True)
    gasComposition = models.OneToOneField(Gas, help_text='г/с', on_delete=models.CASCADE, null=True)


# class Formulas(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     date = models.CharField(default=None, max_length=50, null=True)
#     NO2 = models.CharField(default='V*%NO2m*p', max_length=50, null=True)

