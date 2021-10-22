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
            cls.model_serializer = FacilityRequest.CompSer
        elif path == '/object/powerplant/':
            cls.model = PowerPlant
            cls.model_serializer = FacilityRequest.PPSer
        else:
            cls.model = Boiler
            cls.model_serializer = FacilityRequest.BoilSer


def get_facility(cls, request) -> Response:
    FacilityRequest(cls, request)
    try:
        obj = cls.model.objects.get()
        serializer = cls.model_serializer(obj)
        return Response(serializer.data, status.HTTP_200_OK)
    except cls.model.DoesNotExist:
        return Response({'date': None})


def create_facility(cls, request) -> Response:
    path = request.get_full_path()

    FacilityRequest(cls, request)
    facility_name = path.split('/')[2]

    gas_name = get_gas_name(facility_name)
    gas_composition = Gas.objects.get_or_create(gasName=gas_name)[0]

    obj = cls.model(**request.data)
    obj.date = datetime.datetime.now()
    obj.gasComposition = gas_composition
    gas_composition.save()

    token = request.headers['Authorization'].split(' ')[1]
    data_token = jwt.decode(
        token, settings.ACCESS_SECRET_KEY, algorithms='HS256'
    )
    current_user = User.objects.get(email=data_token['email'])
    obj.user = current_user
    obj.save()

    return get_facility(cls, request)


def set_refusal_data(cls, request):
    FacilityRequest(cls, request)
    refusal_data = get_refusal_data(request)
    cls.model.objects.all().update(
        refusalData=refusal_data, user=None, date=None, isEdited=False
    )
    return get_summary_data()


def edit_data(cls, request) -> Response:
    FacilityRequest(cls, request)
    obj = cls.model.objects.all()
    obj.update(**request.data)
    obj = cls.model.objects.get()
    current_user = get_current_user(request)
    obj.date = datetime.datetime.now()
    obj.user = current_user
    obj.isEdited = True
    obj.refusalData = {'date': None}
    obj.save()
    obj = cls.model.objects.get()
    serializer = cls.model_serializer(obj)
    return Response(serializer.data, status.HTTP_200_OK)
