from rest_framework import status
from rest_framework.response import Response
from backend.models import GasComposition, Compressor, PowerPlant, Boiler
from backend.serializers import CompressorSerializer, PowerPlantSerializer, BoilerSerializer


class FacilityRequest:
    def __init__(self, request, cls):
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


def create_facility(request, path, model, model_serializer):
    facility_name = path.split('/')[2]
    gasComposition = GasComposition.objects.get_or_create(facilityName=facility_name)[0]
    facility = model(**request.data)
    facility.gasComposition = gasComposition
    gasComposition.save()
    facility.save()
    obj = model.objects.first()
    serializer = model_serializer(obj)
    return Response(serializer.data, status.HTTP_200_OK)
