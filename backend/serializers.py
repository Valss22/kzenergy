from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from backend.models import *


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('excel',)
