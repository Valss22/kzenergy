import jwt
from rest_framework.permissions import BasePermission

from social_network import settings


class IsAuth(BasePermission):
    def has_permission(self, request, view) -> bool:
        try:
            token = request.headers['Authorization'].split(' ')[1]
            jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
            return True
        except jwt.ExpiredSignatureError:
            return False
