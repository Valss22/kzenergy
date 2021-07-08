import time
import jwt
import bcrypt
from rest_framework import status
from rest_framework.response import Response

from kzenergy import settings
from backend.models import *
from kzenergy.settings import SALT


class AuthResponce:
    def __init__(self, payload_access, request):
        email = request.data['email']
        access = jwt.encode(payload_access,
                            settings.ACCESS_SECRET_KEY, algorithm='HS256')
        # refresh = jwt.encode(payload_refresh,
        #                      settings.REFRESH_SECRET_KEY, algorithm='HS256')
        # refresh = str(refresh)[2:-1]
        self.response = Response()
        # self.response.set_cookie(key='refresh', value=refresh, httponly=True)
        self.response.data = {
            'id': User.objects.get(email=email).id,
            'access': access,
            'email': email
        }
        if 'role' and 'fullName' in request.data.keys():
            self.response.data.update({'role': request.data['role'],
                                       'fullName': request.data['fullName']})
        else:
            user = User.objects.get(email=email)
            d = {'role': user.role, 'fullName': user.fullName}
            self.response.data.update(d)


class UserData:
    def __init__(self, request):
        self.email = request.data['email']
        hached = bcrypt.hashpw(request.data['password'].encode(), SALT)
        self.password = hached
        if 'fullName' and 'role' in request.data.keys():
            self.fullName = request.data['fullName']
            self.role = request.data['role']
        self.payload_access = {
            'email': self.email,
            'exp': time.time() + 30
        }
        # self.payload_refresh = {
        #     'email': self.email,
        #     'exp': time.time() + 86400
        # }


def create_user(user: UserData, request) -> Response:
    if not validate_role(user.role):
        return Response({'error': f'{user.role} is not a exists role'}, status.HTTP_400_BAD_REQUEST)
    userObj = User.objects.create(fullName=user.fullName, email=user.email,
                                  password=user.password, role=user.role)
    userObj.save()
    # UserRefreshToken.objects.create(user=userObj, refresh=request.COOKIES['refresh'])
    authResponce = AuthResponce(user.payload_access, request)
    return authResponce.response


def sign_in(request):
    user = UserData(request)
    try:
        User.objects.get(email=user.email)
        return Response({'error': 'User already exist'}, status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        if request.data['identificationKey'] == settings.IDENTIFICATION_KEY:
            return create_user(user, request)
        return Response({'error': 'Registration failed'}, status.HTTP_400_BAD_REQUEST)


def login(request):
    user = UserData(request)
    try:
        hashed_pass = User.objects.get(email=request.data['email']).password[2:-1].encode()
        current_pass = request.data['password'].encode()
        if bcrypt.checkpw(current_pass, hashed_pass):
            authResponce = AuthResponce(user.payload_access, request)
            return authResponce.response
        return Response({'error': 'Auth failed'}, status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'Auth failed'}, status.HTTP_400_BAD_REQUEST)
