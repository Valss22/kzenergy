from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from backend.permissions import IsCreated, IsAuth
from backend.serializers import *
from backend.services.auth import *
from backend.services.compressor import create_compressor
from backend.services.facility import create_facility, FacilityRequest


class SignInView(APIView):

    def post(self, request):
        return sign_in(request)


class LoginView(APIView):

    def post(self, request):
        return login(request)


class FacilityView(APIView):
    permission_classes = [IsAuth, IsCreated]

    model = None
    model_serializer = None

    @classmethod
    def get(cls, request):
        FacilityRequest(request, cls)
        obj = cls.model.objects.first()
        serializer = cls.model_serializer(obj)
        return Response(serializer.data, status.HTTP_200_OK)

    @classmethod
    def post(cls, request):
        path = request.get_full_path()
        FacilityRequest(request, cls)
        return create_facility(request, path, cls.model, cls.model_serializer)


class GasCompositionViewSet(ReadOnlyModelViewSet):
    queryset = GasComposition.objects.all()
    serializer_class = GasCompositionSerializer

