from rest_framework.serializers import ModelSerializer
from backend.models import *
from backend.parsing import parse_date
from rest_framework import serializers


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('excel',)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('fullName', 'id')


class FacilitySerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    def to_representation(self, data):
        data = super().to_representation(data)
        data['date'] = parse_date(data['date'])
        return data


class GasSerializerAllField(FacilitySerializer):
    class Meta:
        model = Gas
        fields = '__all__'


class GasSerializerOneField(ModelSerializer):
    class Meta:
        model = Gas
        fields = ('gasName',)


class CompressorSerializerAllField(FacilitySerializer):
    gasComposition = GasSerializerOneField(read_only=True)

    class Meta:
        model = Compressor
        fields = '__all__'


class CompressorSerializerOneField(FacilitySerializer):
    class Meta:
        model = Compressor
        fields = ('date',)


class PowerPlantSerializerAllField(FacilitySerializer):
    gasComposition = GasSerializerOneField(read_only=True)

    class Meta:
        model = PowerPlant
        fields = '__all__'


class PowerPlantSerializerOneField(FacilitySerializer):
    class Meta:
        model = PowerPlant
        fields = ('date',)


class BoilerSerializerAllField(FacilitySerializer):
    gasComposition = GasSerializerOneField(read_only=True)

    class Meta:
        model = Boiler
        fields = '__all__'


class BoilerSerializerOneField(FacilitySerializer):
    class Meta:
        model = Boiler
        fields = ('date',)


class FormulasSerializer(FacilitySerializer):
    compressor = serializers.SerializerMethodField()

    class Meta:
        model = Formulas
        fields = '__all__'

    def get_compressor(self, instance):
        V = Compressor.objects.get().gasConsumptionVolume
        return V
