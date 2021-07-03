import time
import jwt
from rest_framework import status
from rest_framework.response import Response
from kzenergy import settings
from backend.models import *


class AuthToken:
    def __init__(self, payload_access, request):
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
        self.email = request.data['email']
        self.password = request.data['password']
        if 'fullName' and 'role' in request.data.keys():
            self.fullName = request.data['fullName']
            self.role = request.data['role']
        self.payload = {
            'email': self.email,
            'exp': time.time() + 86400
        }


def create_user(user: UserData, request) -> Response:
    userObj = User.objects.create(full_name=user.fullName, email=user.email,
                                  password=user.password, role=user.role)
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
    try:
        User.objects.get(email=user.email)
        token = AuthToken(user.payload, request)
        return token.response
    except User.DoesNotExist:
        return Response({'error': 'Auth failed'}, status.HTTP_400_BAD_REQUEST)

