from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from backend.models import Compressor, PowerPlant, Boiler, Gas
from backend.serializers import CompressorSerializerAllField, CompressorSerializerOneField, \
    PowerPlantSerializerAllField, PowerPlantSerializerOneField, BoilerSerializerAllField, BoilerSerializerOneField, \
    GasSerializerAllField


def get_summary_data() -> Response:
    compObj = Compressor.objects.all().first()
    ppObj = PowerPlant.objects.all().first()
    boilObj = Boiler.objects.all().first()

    try:
        Compressor.objects.get()
        compSer = CompressorSerializerAllField(compObj)
    except Compressor.DoesNotExist:
        compSer = CompressorSerializerOneField(compObj)

    try:
        PowerPlant.objects.get()
        ppSer = PowerPlantSerializerAllField(ppObj)
    except PowerPlant.DoesNotExist:
        ppSer = PowerPlantSerializerOneField(ppObj)

    try:
        Boiler.objects.get()
        boilSer = BoilerSerializerAllField(boilObj)
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
                    fields = ('date',)

            gasSer = GasSer(gasObj)
            gasDict[i] = gasSer.data
            continue

        gasSer = GasSerializerAllField(gasObj)
        gasDict[i] = gasSer.data

    # gases = []
    # for value in gasDict.values():
    #     gases.append(value)

    print(gasDict)

    return Response({
        'compressor': compSer.data,
        'powerPlant': ppSer.data,
        'boiler': boilSer.data,
        'gases': gasDict,
    }, status.HTTP_200_OK)
