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


class GasCompositionSerializer(ModelSerializer):
    class Meta:
        model = GasComposition
        fields = ('gasName',)


class CompressorSerializer(FacilitySerializer):
    class Meta:
        model = Compressor
        exclude = ('gasComposition',)


class PowerPlantSerializer(FacilitySerializer):
    class Meta:
        model = PowerPlant
        exclude = ('gasComposition',)


class BoilerSerializer(FacilitySerializer):
    class Meta:
        model = Boiler
        exclude = ('gasComposition',)


class CompressorSerializer3Group(FacilitySerializer):
    gasComposition = GasCompositionSerializer(read_only=True)

    class Meta:
        model = Compressor
        try:
            Compressor.objects.get()

            fields = '__all__'
        except Compressor.DoesNotExist:
            fields = ''


class PowerPlantSerializer3Group(FacilitySerializer):
    gasComposition = GasCompositionSerializer(read_only=True)

    class Meta:
        model = PowerPlant
        try:
            PowerPlant.objects.get()

            fields = '__all__'
        except PowerPlant.DoesNotExist:
            fields = ''


class BoilerSerializer3Group(FacilitySerializer):
    gasComposition = GasCompositionSerializer(read_only=True)

    class Meta:
        model = Boiler
        try:
            Boiler.objects.get()
            fields = '__all__'
        except Boiler.DoesNotExist:
            fields = ''
