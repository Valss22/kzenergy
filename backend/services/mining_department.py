import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from backend.models import Compressor, PowerPlant, Boiler, Gas, Formulas
from backend.parsing import parse_date
from backend.serializers import CompressorSerializerAllField, CompressorSerializerOneField, \
    PowerPlantSerializerAllField, PowerPlantSerializerOneField, BoilerSerializerAllField, BoilerSerializerOneField, \
    GasSerializerAllField
from backend.services.auth import get_current_user


def get_summary_data() -> Response:
    count: int = 0  # Счетчик по заполнению

    compObj = Compressor.objects.all().first()
    ppObj = PowerPlant.objects.all().first()
    boilObj = Boiler.objects.all().first()

    try:
        obj = Compressor.objects.get()
        if obj.date is None:
            class CompSer(ModelSerializer):
                class Meta:
                    model = Compressor
                    fields = ('date', 'refusalData')
            compSer = CompSer(compObj)
        else:
            compSer = CompressorSerializerAllField(compObj)
            count += 1
    except Compressor.DoesNotExist:
        compSer = CompressorSerializerOneField(compObj)

    try:
        obj = PowerPlant.objects.get()
        if obj.date is None:
            class PPSer(ModelSerializer):
                class Meta:
                    model = PowerPlant
                    fields = ('date', 'refusalData')

            ppSer = PPSer(ppObj)
        else:
            ppSer = PowerPlantSerializerAllField(ppObj)
            count += 1
    except PowerPlant.DoesNotExist:
        ppSer = PowerPlantSerializerOneField(ppObj)

    try:
        obj = Boiler.objects.get()
        if obj.date is None:
            class BoilSer(ModelSerializer):
                class Meta:
                    model = Boiler
                    fields = ('date', 'refusalData')

            boilSer = BoilSer(ppObj)
        else:
            boilSer = BoilerSerializerAllField(boilObj)
            count += 1
    except Boiler.DoesNotExist:
        boilSer = BoilerSerializerOneField(boilObj)

    gasNames = [obj.gasName for obj in Gas.objects.all()]

    gasDict = {}

    for i in gasNames:
        gasObj = Gas.objects.get(gasName=i)

        if gasObj.date is None:
            class GasSer(ModelSerializer):
                class Meta:
                    model = Gas
                    fields = ('date', 'refusalData')

            gasSer = GasSer(gasObj)
            gasDict[i] = gasSer.data
            continue

        count += 1
        gasSer = GasSerializerAllField(gasObj)
        gasDict[i] = gasSer.data

    if not gasDict:
        gasDict['sweetGas'] = {'date': None}

    user = Formulas.objects.get().user
    date = Formulas.objects.get().date
    isConfirmed = Formulas.objects.get().isConfirmed

    if user is not None:
        user = {'fullName': user.fullName,
                'id': user.id}

    date = parse_date(date)

    responce = Response()

    responce.data = {
        'compressor': compSer.data,
        'powerplant': ppSer.data,
        'boiler': boilSer.data,
        'gases': gasDict,
    }

    isConfirmable = True

    print(count)
    print(len(responce.data.keys()))

    if count != len(responce.data.keys()) or isConfirmed:
        isConfirmable = False

    confirmData = {
        'user': user,
        'date': date,
        'isConfirmed': isConfirmed,
        'isConfirmable': isConfirmable
    }

    responce.data['confirmData'] = confirmData

    return responce


def sign_report(request):
    currentUser = get_current_user(request)
    Formulas.objects.all().update(user=currentUser,
                                  date=datetime.datetime.now(),
                                  isConfirmed=True)
    return get_summary_data()
