import jwt
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from backend.models import *
from social_network import settings


class UserProfileSerializer(ModelSerializer):
    username = serializers.SerializerMethodField()
    isFollowed = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        exclude = ('user', 'subscriptions')

    def get_username(self, instance):
        return instance.user.username

    def get_isFollowed(self, instance):
        #token = self.context.get('request', None).headers['Authorization'].split(' ')[1]
        #token = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
        #if token['name'] == instance.user.username:
            #return True
        return False


