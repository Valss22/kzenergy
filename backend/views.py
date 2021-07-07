from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from backend.permissions import IsCreated
from backend.serializers import *
from backend.services.auth import *
from backend.services.compressor import create_compressor


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
        return Response(serializer.data, status.HTTP_200_OK)


class CreateCompressorView(APIView):
    permission_classes = [IsCreated]

    def post(self, request):
        return create_compressor(request)
