from rest_framework.views import APIView

from backend.serializers import UserProfileSerializer
from backend.services.auth import *
from rest_framework import viewsets


class SignInView(APIView):

    def post(self, request):
        return sign_in(request)


class LoginView(APIView):

    def post(self, request):
        return login(request)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

