import datetime

import jwt
from rest_framework import status
from rest_framework.response import Response

from backend.models import User, Gas
from backend.serializers import GasSerializerAllField
from kzenergy import settings


def get_gas_name(facility_name: str):
    if facility_name in ['compressor', 'powerplant', 'boiler']:  # TODO: Синхронизация с URL
        return 'sweetGas'


def get_gas(request, model, model_serializer):
    try:
        obj = model.objects.get(gasName=request.query_params['gasName'])
        serializer = model_serializer(obj)
        return Response(serializer.data, status.HTTP_200_OK)
    except model.DoesNotExist:
        return Response({'date': None})


def update_gas(request):
    gasComposition = Gas.objects.filter(gasName=request.data['gasName'])
    gasComposition.update(**request.data)


def create_gas(request):
    if Gas.objects.filter(gasName=request.data['gasName']).exists():
        update_gas(request)
    else:
        obj = Gas(**request.data)
        obj.date = datetime.datetime.now()
        token = request.headers['Authorization'].split(' ')[1]
        dataToken = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
        currentUser = User.objects.get(email=dataToken['email'])
        obj.user = currentUser
        obj.save()
    try:
        obj = Gas.objects.get(gasName=request.data['gasName'])
        serializer = GasSerializerAllField(obj)
        return Response(serializer.data, status.HTTP_200_OK)
    except Gas.DoesNotExist:
        return Response({'date': None})
