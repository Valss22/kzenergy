from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from backend.permissions import IsCreated, IsAuth
from backend.serializers import *
from backend.services.auth import *
from backend.services.compressor import create_compressor
from backend.services.facility import create_facility


class SignInView(APIView):

    def post(self, request):
        return sign_in(request)


class LoginView(APIView):

    def post(self, request):
        return login(request)


class FacilityView(APIView):
    permission_classes = [IsAuth]  # TODO исправить мидл для гет запроса

    model = None
    model_serializer = None

    @classmethod
    def get(cls, request):
        path = request.get_full_path()

        if path == '/object/compressor/':
            cls.model = Compressor
            cls.model_serializer = CompressorSerializer
        elif path == '/object/powerplant/':
            cls.model = PowerPlant
            cls.model_serializer = PowerPlantSerializer
        else:
            cls.model = Boiler
            cls.model_serializer = BoilerSerializer

        obj = cls.model.objects.first()
        serializer = cls.model_serializer(obj)
        return Response(serializer.data, status.HTTP_200_OK)

    @classmethod
    def post(cls, request):
        path = request.get_full_path()

        if path == '/object/compressor/':
            cls.model = Compressor
            cls.model_serializer = CompressorSerializer
        elif path == '/object/powerplant/':
            cls.model = PowerPlant
            cls.model_serializer = PowerPlantSerializer
        else:
            cls.model = Boiler
            cls.model_serializer = BoilerSerializer

        return create_facility(request, path, cls.model, cls.model_serializer)


class GasCompositionViewSet(ReadOnlyModelViewSet):
    queryset = GasComposition.objects.all()
    serializer_class = GasCompositionSerializer

# class CreateCompressorView(APIView):
#     permission_classes = [IsCreated]
#     model = Compressor
#
#     def post(self, request):
#         return create_compressor(request)


# class CreateFacilityView(APIView):
#     permission_classes = [IsAuth, IsCreated]
#     model = None
#     model_serializer = None
#
#     @classmethod
#     def post(cls, request):
#         path = request.get_full_path()
#
#         if path == '/object/compressor/':
#             cls.model = Compressor
#             cls.model_serializer = CompressorSerializer
#         elif path == '/object/powerplant/':
#             cls.model = PowerPlant
#             cls.model_serializer = PowerPlantSerializer
#         else:
#             cls.model = Boiler
#             cls.model_serializer = BoilerSerializer
#
#         return create_facility(request, path, cls.model, cls.model_serializer)
