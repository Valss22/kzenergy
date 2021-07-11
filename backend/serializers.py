from rest_framework.serializers import ModelSerializer
from backend.models import *
from backend.parsing import parse_date


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('excel',)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('fullName',)


class FacilitySerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    def to_representation(self, data):
        data = super().to_representation(data)
        data['date'] = parse_date(data['date'])
        return data


class CompressorSerializer(FacilitySerializer):
    class Meta:
        model = Compressor
        exclude = ('gasComposition',)


class PowerPlantSerializer(FacilitySerializer):
    class Meta:
        model = PowerPlant
        exclude = ('actualPower', 'gasComposition')


class BoilerSerializer(FacilitySerializer):
    class Meta:
        model = Boiler
        fields = ('id', 'date', 'user', 'gasConsumptionVolume',
                  'steamVolume', 'workingHours')


class GasCompositionSerializer(FacilitySerializer):
    class Meta:
        model = GasComposition
        fields = '__all__'

    # def to_representation(self, data):
    #     data = super().to_representation(data)
    #     data['date'] = parse_date(data['date'], 'GET-LIST')
    #     return data
