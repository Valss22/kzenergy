import jwt
from rest_framework import status

from backend.models import Gas, Compressor, PowerPlant, Boiler, User
from backend.serializers import FacilitySerializer
from backend.services.gas import get_gas_name
from rest_framework.response import Response

from kzenergy import settings


class FacilityRequest:
    class CompSer(FacilitySerializer):
        class Meta:
            model = Compressor
            exclude = ('gasComposition',)

    class PPSer(FacilitySerializer):
        class Meta:
            model = PowerPlant
            exclude = ('gasComposition',)

    class BoilSer(FacilitySerializer):
        class Meta:
            model = Boiler
            exclude = ('gasComposition',)

    def __init__(self, cls, request):
        path = request.get_full_path()
        if path == '/object/compressor/':
            cls.model = Compressor
            cls.modelSerializer = FacilityRequest.CompSer
        elif path == '/object/powerplant/':
            cls.model = PowerPlant
            cls.modelSerializer = FacilityRequest.PPSer
        else:
            cls.model = Boiler
            cls.modelSerializer = FacilityRequest.BoilSer


def get_facility(cls, request):
    FacilityRequest(cls, request)
    try:
        obj = cls.model.objects.get()
        serializer = cls.modelSerializer(obj)
        return Response(serializer.data, status.HTTP_200_OK)
    except cls.model.DoesNotExist:
        return Response({'date': None})


def create_facility(cls, request):
    path = request.get_full_path()

    FacilityRequest(cls, request)
    facilityName = path.split('/')[2]

    gasName = get_gas_name(facilityName)
    gasComposition = Gas.objects.get_or_create(gasName=gasName)[0]
    # TODO: создать запись для хим. лабы и записать в связанное поле только при запросе со второй группы!!!
    obj = cls.model(**request.data)
    obj.gasComposition = gasComposition
    gasComposition.save()

    token = request.headers['Authorization'].split(' ')[1]
    dataToken = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
    currentUser = User.objects.get(email=dataToken['email'])
    obj.user = currentUser
    obj.save()

    return get_facility(cls, request)
