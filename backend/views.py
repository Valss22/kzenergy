from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from backend.serializers import *
from backend.services.auth import *


class SignInView(APIView):

    def post(self, request):
        return sign_in(request)


class LoginView(APIView):

    def post(self, request):
        return login(request)


class UserProfileViewSet(ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CompressorView(APIView):

    def get(self, request):
        obj = Compressor.objects.first()
        serializer = CompressorSerializer(obj)
        return Response(serializer.data)
