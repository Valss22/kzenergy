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
        return f'{self.fullName}({self.email}({self.id}))'


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


class GasComposition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=datetime.datetime.now(), null=True)
    facilityName = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.facilityName}({self.id})'


class Compressor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=datetime.datetime.now(), null=True)
    gasConsumptionVolume = models.FloatField(help_text='тыс. м3', null=True)
    volumeOfInjectedGas = models.FloatField(help_text='тыс. м3', null=True)
    workingHours = models.FloatField(help_text='часы', null=True)
    gasComposition = models.OneToOneField(GasComposition,
                                          help_text='г/с', on_delete=models.CASCADE, null=True)
    wasteGases = models.FloatField(help_text='г/с', null=True)


class PowerPlant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=datetime.datetime.now(), null=True)
    gasConsumptionVolume = models.FloatField(help_text='тыс. м3', null=True)
    generatedElectricity = models.FloatField(help_text='МВт*ч', null=True)
    workingHours = models.FloatField(help_text='часы', null=True)
    gasComposition = models.OneToOneField(GasComposition,
                                          help_text='г/с', on_delete=models.CASCADE, null=True)
    actualPower = models.FloatField(help_text='МВт', null=True)


class Boiler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=datetime.datetime.now(), null=True)
    gasConsumptionVolume = models.FloatField(help_text='тыс. м3', null=True)
    steamVolume = models.FloatField(help_text='т', null=True)
    workingHours = models.FloatField(help_text='часы', null=True)
    gasComposition = models.OneToOneField(GasComposition,
                                          help_text='г/с', on_delete=models.CASCADE, null=True)
    actualPower = models.FloatField(help_text='МВт', null=True)
    wasteGases = models.FloatField(help_text='г/с', null=True)
    EnthalpySteam = models.FloatField(help_text='кДж/кг', null=True)
    EnthalpyWater = models.FloatField(help_text='кДж/кг', null=True)
    LowerHeatCombustion = models.FloatField(help_text='ТГ, кДж/м3', null=True)
    LowerHeatCombustionNC = models.FloatField(help_text='ТГ при НУ, кДж/м3', null=True)
