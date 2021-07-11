import jwt
from rest_framework import status
from rest_framework.response import Response

from backend.models import User
from kzenergy import settings

import datetime


def get_gas_name(facility_name: str):
    if facility_name in ['compressor', 'powerPlant', 'boiler']:
        return 'sweetGas'


def update_gas_composition(request, model):
    gasComposition = model.objects.filter(gasName=request.data['gasName'])
    gasComposition.update(**request.data)


def create_gas_composition(request, model, model_serializer):

    if model.objects.filter(gasName=request.data['gasName']).exists():
        update_gas_composition(request, model)
        obj = model.objects.get(gasName=request.data['gasName'])
        serializer = model_serializer(obj)
        return Response(serializer.data, status.HTTP_200_OK)

    gasComposition = model(**request.data)
    token = request.headers['Authorization'].split(' ')[1]
    dataToken = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
    currentUser = User.objects.get(email=dataToken['email'])
    gasComposition.user = currentUser
    gasComposition.date = datetime.datetime.now()
    gasComposition.save()
    obj = model.objects.get(gasName=request.data['gasName'])
    serializer = model_serializer(obj)
    return Response(serializer.data, status.HTTP_200_OK)
