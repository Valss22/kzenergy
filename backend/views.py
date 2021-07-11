from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from backend.permissions import IsCreated, IsAuth
from backend.serializers import *
from backend.services.auth import *
from backend.services.facility import create_facility, FacilityRequest
from backend.services.gas_composition import create_gas_composition


class SignInView(APIView):

    def post(self, request):
        return sign_in(request)


class LoginView(APIView):

    def post(self, request):
        return login(request)


class FacilityView(APIView):
    # permission_classes = [IsAuth, IsCreated]

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


class GasCompositionView(APIView):
    permission_classes = [IsAuth]

    def get(self, request):
        gasName = request.query_params['gasName']
        try:
            obj = GasComposition.objects.get(gasName=gasName)
            serializer = GasCompositionSerializer(obj)
            return Response(serializer.data, status.HTTP_200_OK)
        except GasComposition.DoesNotExist:
            return Response({'date': None})

    def post(self, request):
        return create_gas_composition(request, GasComposition, GasCompositionSerializer)
