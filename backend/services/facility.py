import jwt
import datetime
from rest_framework import status

from backend.models import Gas, Compressor, PowerPlant, Boiler, User

from backend.serializers import FacilitySerializer
from backend.services.auth import get_current_user
from backend.services.common import get_refusal_data
from backend.services.gas import get_gas_name
from rest_framework.response import Response

from backend.services.mining_department import get_summary_data
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


def get_facility(cls, request) -> Response:
    FacilityRequest(cls, request)
    try:
        obj = cls.model.objects.get()
        serializer = cls.modelSerializer(obj)
        return Response(serializer.data, status.HTTP_200_OK)
    except cls.model.DoesNotExist:
        return Response({'date': None})


def create_facility(cls, request) -> Response:
    path = request.get_full_path()

    FacilityRequest(cls, request)
    facilityName = path.split('/')[2]

    gasName = get_gas_name(facilityName)
    gasComposition = Gas.objects.get_or_create(gasName=gasName)[0]

    obj = cls.model(**request.data)
    obj.date = datetime.datetime.now()
    obj.gasComposition = gasComposition
    gasComposition.save()

    token = request.headers['Authorization'].split(' ')[1]
    dataToken = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
    currentUser = User.objects.get(email=dataToken['email'])
    obj.user = currentUser
    obj.save()

    return get_facility(cls, request)


def set_refusal_data(cls, request):
    FacilityRequest(cls, request)
    refusalData = get_refusal_data(request)
    cls.model.objects.all().update(refusalData=refusalData,
                                   user=None, date=None)
    return get_summary_data()


def edit_data(cls, request) -> Response:
    FacilityRequest(cls, request)
    obj = cls.model.objects.all()
    obj.update(**request.data)
    obj = cls.model.objects.get()
    currentUser = get_current_user(request)
    obj.date = datetime.datetime.now()
    obj.user = currentUser
    obj.isEdited = True
    obj.refusalData = {'date': None}
    obj.save()
    obj = cls.model.objects.get()
    serializer = cls.modelSerializer(obj)
    return Response(serializer.data, status.HTTP_200_OK)


