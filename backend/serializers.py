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
        exclude = ('gasComposition',)

    def to_representation(self, data):
        data = super().to_representation(data)
        data['date'] = parse_date(data['date'])
        return data
