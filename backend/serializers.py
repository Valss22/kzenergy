from rest_framework.serializers import ModelSerializer
from backend.models import *
from backend.parsing import parse_date


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('excel',)


class CompressorSerializer(ModelSerializer):
    class Meta:
        model = Compressor
        exclude = ('gasComposition', 'wasteGases')

    def to_representation(self, data):
        data = super().to_representation(data)
        data['date'] = parse_date(data['date'])
        return data


class PowerPlantSerializer(ModelSerializer):
    class Meta:
        model = PowerPlant
        exclude = ('actualPower', 'gasComposition')


class BoilerSerializer(ModelSerializer):
    class Meta:
        model = Boiler
        fields = ('id', 'date', 'user', 'gasConsumptionVolume',
                  'steamVolume', 'workingHours')


class GasCompositionSerializer(ModelSerializer):
    class Meta:
        model = GasComposition
        fields = '__all__'

    def to_representation(self, data):
        data = super().to_representation(data)
        data['date'] = parse_date(data['date'], 'GET-LIST')
        return data
