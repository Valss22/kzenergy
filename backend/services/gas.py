import datetime

from rest_framework import status
from rest_framework.response import Response

from backend.models import User, Gas
from backend.serializers import GasSerAllField
from backend.services.auth import get_current_user
from backend.services.common import get_refusal_data
from backend.services.mining_department import get_summary_data


def get_gas_name(facility_name: str):
    if facility_name in ['compressor', 'powerplant', 'boiler']:  # TODO: Синхронизация с URL
        return 'sweetGas'


def get_gas(request):
    try:
        gas_name = request.query_params['gasName']
        obj = Gas.objects.get(gasName=gas_name)
        serializer = GasSerAllField(obj)

        return Response(
            serializer.data, status.HTTP_200_OK
        )
    except Gas.DoesNotExist:
        return Response({'date': None})


def update_gas(request):
    gas_name = request.data['gasName']
    obj = Gas.objects.filter(gasName=gas_name)
    obj.update(**request.data)
    gas = Gas.objects.get(gasName=request.data['gasName'])
    current_user = get_current_user(request)
    gas.date = datetime.datetime.now()
    gas.user = current_user
    gas.save()


def create_gas(request):
    if Gas.objects.filter(gasName=request.data['gasName']).exists():
        update_gas(request)
    else:
        obj = Gas(**request.data)
        obj.date = datetime.datetime.now()
        current_user = get_current_user(request)
        obj.user = current_user
        obj.save()
    try:
        obj = Gas.objects.get(
            gasName=request.data['gasName']
        )
        serializer = GasSerAllField(obj)
        return Response(
            serializer.data, status.HTTP_200_OK
        )
    except Gas.DoesNotExist:
        return Response({'date': None})


def set_refusal_gas_data(request):
    refusal_data = get_refusal_data(request)
    gas_name = request.data['gasName']
    Gas.objects.filter(gasName=gas_name) \
        .update(refusalData=refusal_data, date=None,
                user=None, isEdited=False)
    return get_summary_data()


def edit_gas_data(request):
    gas_name = request.data['gasName']
    obj = Gas.objects.filter(gasName=gas_name)
    obj.update(**request.data)
    obj = Gas.objects.get(gasName=gas_name)
    current_user = get_current_user(request)
    obj.date = datetime.datetime.now()
    obj.user = current_user
    obj.isEdited = True
    obj.refusalData = {'date': None}
    obj.save()
    obj = Gas.objects.get(gasName=gas_name)
    serializer = GasSerAllField(obj)
    return Response(serializer.data, status.HTTP_200_OK)
