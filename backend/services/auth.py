import time
import jwt
from rest_framework import status
from rest_framework.response import Response
from kzenergy import settings
from backend.models import *


class AuthToken:
    def __init__(self, payload_access, request):
        self.access = jwt.encode(payload_access,
                                 settings.ACCESS_SECRET_KEY, algorithm='HS256')
        self.response = Response()
        self.response.data = {
            'id': User.objects.get(email=request.data['email']).id,
            'access': self.access,
            'email': request.data['email'],
        }


class UserData:
    def __init__(self, request):
        self.email = request.data['email']
        self.password = request.data['password']
        self.payload = {
            'email': request.data['email'],
            'exp': time.time() + 86400
        }


def sign_in(request):
    user = UserData(request)
    try:
        User.objects.get(email=user.email)
        return Response({'error': 'user already exist'},
                        status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        ind = user.email.find('@')
        username = user.email[:ind]
        userObj = User.objects.create(username=username, email=user.email,
                                      password=user.password)
        userObj.save()
        UserProfile.objects.create(user=userObj)
        token = AuthToken(user.payload, request)
        return token.response


def login(request):
    user = UserData(request)
    try:
        User.objects.get(email=user.email, password=user.password)
        token = AuthToken(user.payload, request)
        return token.response
    except User.DoesNotExist:
        return Response({'error': 'auth failed'},
                        status=status.HTTP_400_BAD_REQUEST)
