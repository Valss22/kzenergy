import jwt
from rest_framework.permissions import BasePermission
from backend.models import Compressor, PowerPlant, Boiler
from kzenergy import settings


class IsAuth(BasePermission):
    def has_permission(self, request, view) -> bool:
        try:
            token = request.headers['Authorization'].split(' ')[1]
            jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
            return True
        except jwt.ExpiredSignatureError:
            return False


class IsCreated(BasePermission):

    def has_permission(self, request, view) -> bool:
        path = request.get_full_path()

        if path == '/object/compressor/':
            model = Compressor
        elif path == '/object/powerplant/':
            model = PowerPlant
        else:
            model = Boiler

        if len(model.objects.all()) == 0:
            return True
