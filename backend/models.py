from django.db import models
from cloudinary.models import CloudinaryField
from backend.validators import *


def refusal_data_default() -> dict:
    return {'date': None}


class User(models.Model):
    email = models.EmailField(null=True)
    fullName = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=128, null=True)
    avatar = CloudinaryField(null=True)
    phone = models.CharField(max_length=13, null=True)

    def __str__(self):
        return f'{self.fullName}'


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

    refusalData = models.JSONField(default=refusal_data_default, null=True)
    isEdited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.gasName}({self.id})'


class Compressor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.CharField(default=None, max_length=50, null=True)
    gasConsumptionVolume = models.FloatField(help_text='тыс. м3', null=True)
    volumeOfInjectedGas = models.FloatField(help_text='тыс. м3', null=True)
    workingHours = models.FloatField(help_text='часы', null=True)
    gasComposition = models.OneToOneField(Gas, help_text='г/с', on_delete=models.CASCADE, null=True)

    refusalData = models.JSONField(default=refusal_data_default, null=True)
    isEdited = models.BooleanField(default=False)


class PowerPlant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.CharField(default=None, max_length=50, null=True)
    gasConsumptionVolume = models.FloatField(help_text='тыс. м3', null=True)
    generatedElectricity = models.FloatField(help_text='МВт*ч', null=True)
    workingHours = models.FloatField(help_text='часы', null=True)
    gasComposition = models.OneToOneField(Gas, help_text='г/с', on_delete=models.CASCADE, null=True)

    refusalData = models.JSONField(default=refusal_data_default, null=True)
    isEdited = models.BooleanField(default=False)


class Boiler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.CharField(default=None, max_length=50, null=True)
    gasConsumptionVolume = models.FloatField(help_text='тыс. м3', null=True)
    steamVolume = models.FloatField(help_text='т', null=True)
    workingHours = models.FloatField(help_text='часы', null=True)
    gasComposition = models.OneToOneField(Gas, help_text='г/с', on_delete=models.CASCADE, null=True)

    refusalData = models.JSONField(default=refusal_data_default, null=True)
    isEdited = models.BooleanField(default=False)


class Formulas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.CharField(default=None, max_length=50, null=True, blank=True)
    isConfirmed = models.BooleanField(default=False)

    NO2coef = models.FloatField(default=1)
    NOcoef = models.FloatField(default=1)
    SO2coef = models.FloatField(default=0.02)
    COcoef = models.FloatField(default=1)

    CO2coef = models.FloatField(default=1)
    CH4coef = models.FloatField(default=1)
    N2Ocoef = models.FloatField(default=1)


class Archive(models.Model):
    compressor = models.JSONField(null=True)
    powerplant = models.JSONField(null=True)
    boiler = models.JSONField(null=True)
    chemical = models.JSONField(null=True)
    mining = models.JSONField(null=True)
    EPWorker = models.JSONField(null=True)
