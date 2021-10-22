import jwt
from rest_framework import status
from rest_framework.permissions import BasePermission
from backend.models import Compressor, PowerPlant, Boiler, Gas, User
from kzenergy import settings
from rest_framework.response import Response


class IsAuth(BasePermission):
    def has_permission(self, request, view) -> bool:
        try:
            token = request.headers['Authorization'].split(' ')[1]
            jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
            return True
        except:  # TODO отрегулировать перехват
            return False


class IsRightRole(BasePermission):
    def has_permission(self, request, view) -> bool:
        path = request.get_full_path()
        role_name = path.split('/')[-2]

        token = request.headers['Authorization'].split(' ')[1]
        data_token = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
        current_user = User.objects.get(email=data_token['email'])

        if request.method == 'PATCH':
            if current_user.role == 'mining':
                return True
        else:
            if role_name == current_user.role:
                return True


def model_for_path(request):
    path = request.get_full_path()
    if path == '/object/compressor/':
        model = Compressor
    elif path == '/object/powerplant/':
        model = PowerPlant
    elif path == '/object/boiler/':
        model = Boiler
    else:
        raise ValueError
    return model


def enable_to_edit(func):

    def wrapper(cls, request):
        model = model_for_path(request)
        obj = model.objects.all().first()

        if obj.isEdited:
            return Response(
                {'error': 'This obj already edited'},
                status.HTTP_403_FORBIDDEN
            )
        return func(cls, request)

    return wrapper


def enable_to_edit_gas(func):

    def wrapper(cls, request):
        obj = Gas.objects.get(gasName=request.data['gasName'])
        if obj.isEdited:
            return Response(
                {'error': 'This gas already edited'},
                status.HTTP_403_FORBIDDEN
            )
        return func(cls, request)

    return wrapper


def enable_to_create(func):
    def wrapper(cls, request):
        model = model_for_path(request)

        if len(model.objects.all()) > 0:
            return Response(
                {'error': 'This obj already exists'},status.HTTP_403_FORBIDDEN
            )

        return func(cls, request)

    return wrapper


class IsGasExists(BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.method == 'POST':
            try:
                gas = Gas.objects.get(gasName=request.data['gasName'])
                if gas.date is not None:
                    return False
                return True
            except Gas.DoesNotExist:
                return True
        return True
