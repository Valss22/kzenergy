import datetime

import jwt
from rest_framework import status
from rest_framework.response import Response

from backend.models import User, Gas
from backend.serializers import GasSerializerAllField
from backend.services.auth import get_current_user
from backend.services.common import get_refusal_data
from backend.services.mining_department import get_summary_data


def get_gas_name(facility_name: str):
    if facility_name in ['compressor', 'powerplant', 'boiler']:  # TODO: Синхронизация с URL
        return 'sweetGas'


def get_gas(request):
    try:
        gasName = request.query_params['gasName']
        obj = Gas.objects.get(gasName=gasName)
        serializer = GasSerializerAllField(obj)
        return Response(serializer.data, status.HTTP_200_OK)
    except Gas.DoesNotExist:
        return Response({'date': None})


def update_gas(request):
    gasName = request.data['gasName']
    obj = Gas.objects.filter(gasName=gasName)
    obj.update(**request.data)
    gas = Gas.objects.get(gasName=request.data['gasName'])
    currentUser = get_current_user(request)
    gas.date = datetime.datetime.now()
    gas.user = currentUser
    gas.save()


def create_gas(request):
    if Gas.objects.filter(gasName=request.data['gasName']).exists():
        update_gas(request)
    else:
        obj = Gas(**request.data)
        obj.date = datetime.datetime.now()
        currentUser = get_current_user(request)
        obj.user = currentUser
        obj.save()
    try:
        obj = Gas.objects.get(gasName=request.data['gasName'])
        serializer = GasSerializerAllField(obj)
        return Response(serializer.data, status.HTTP_200_OK)
    except Gas.DoesNotExist:
        return Response({'date': None})


def set_refusal_gas_data(request):
    refusalData = get_refusal_data(request)
    gasName = request.data['gasName']
    Gas.objects.filter(gasName=gasName).update(refusalData=refusalData,
                                               date=None, user=None)
    return get_summary_data()


def edit_gas_data(request):
    gasName = request.data['gasName']
    obj = Gas.objects.filter(gasName=gasName)
    obj.update(**request.data)
    obj = Gas.objects.get(gasName=gasName)
    currentUser = get_current_user(request)
    obj.date = datetime.datetime.now()
    obj.user = currentUser
    obj.isEdited = True
    obj.refusalData = {'date': None}
    obj.save()
    obj = Gas.objects.get(gasName=gasName)
    serializer = GasSerializerAllField(obj)
    return Response(serializer.data, status.HTTP_200_OK)
