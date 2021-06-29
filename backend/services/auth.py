import time
import jwt
from django.core.management.utils import get_random_secret_key
from rest_framework import status
from rest_framework.response import Response
from kzenergy import settings
from backend.models import *


class AuthToken:
    def __init__(self, payload_access, request):
        if 'token' in request.data.keys():
            email = jwt.decode(request.data['token'],
                               settings.ACCESS_SECRET_KEY, algorithms='HS256')
        else:
            email = request.data['email']

        self.access = jwt.encode(payload_access,
                                 settings.ACCESS_SECRET_KEY, algorithm='HS256')
        self.response = Response()
        self.response.data = {
            'id': User.objects.get(email=email).id,
            'access': self.access,
            'email': email,
        }


class UserData:
    def __init__(self, request):
        if 'token' in request.data.keys():
            email = jwt.decode(request.data['token'],
                               settings.ACCESS_SECRET_KEY, algorithms='HS256')
            password = get_random_secret_key()
        else:
            email = request.data['email']
            password = request.data['password']

        self.email = email
        self.password = password
        self.payload = {
            'email': email,
            'exp': time.time() + 86400
        }


def create_user(user: UserData, request) -> Response:
    ind = user.email.find('@')
    username = user.email[:ind]
    userObj = User.objects.create(username=username, email=user.email,
                                  password=user.password)
    userObj.save()
    UserProfile.objects.create(user=userObj)
    token = AuthToken(user.payload, request)
    return token.response


def sign_in(request):
    user = UserData(request)
    try:
        User.objects.get(email=user.email)
        return Response({'error': 'User already exist'},
                        status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return create_user(user, request)


def login(request):
    user = UserData(request)
    if 'token' in request.data.keys():
        try:
            User.objects.get(email=user.email)
            token = AuthToken(user.payload, request)
            return token.response
        except User.DoesNotExist:
            return create_user(user, request)
    try:
        User.objects.get(email=user.email, password=user.password)
        token = AuthToken(user.payload, request)
        return token.response
    except User.DoesNotExist:
        return Response({'error': 'Auth failed'},
                        status=status.HTTP_400_BAD_REQUEST)
