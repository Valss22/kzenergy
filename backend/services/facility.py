import jwt
from rest_framework import status
from rest_framework.response import Response
from backend.models import GasComposition, Compressor, PowerPlant, Boiler, User
from backend.serializers import CompressorSerializer, PowerPlantSerializer, BoilerSerializer
from backend.services.gas_composition import get_gas_name
from kzenergy import settings


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
    facilityName = path.split('/')[2]
    gasName = get_gas_name(facilityName)
    gasComposition = GasComposition.objects.get_or_create(gasName=gasName)[0]
    facility = model(**request.data)
    facility.gasComposition = gasComposition
    token = request.headers['Authorization'].split(' ')[1]
    dataToken = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
    currentUser = User.objects.get(email=dataToken['email'])
    facility.user = currentUser
    gasComposition.save()
    facility.save()
    obj = model.objects.first()
    serializer = model_serializer(obj)
    return Response(serializer.data, status.HTTP_200_OK)
