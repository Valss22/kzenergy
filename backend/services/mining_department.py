import datetime

from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from backend.models import Compressor, PowerPlant, Boiler, Gas, Formulas
from backend.parsing import parse_date
from backend.serializers import CompSerAllField, CompSerOneField, \
    PPSerAllField, PPSerOneField, BoilSerAllField, BoilSerOneField, \
    GasSerAllField, PPSerTwoField, BoilSerTwoField, CompSerTwoField
from backend.services.auth import get_current_user


class FacSerData:

    def __init__(self, facility, fac_ser_two_field, fac_obj,
                 fac_ser_all_field, fac_ser_one_field):
        try:
            obj = facility.objects.get()
            if obj.date is None:
                self.facSer = fac_ser_two_field(fac_obj)
            else:
                self.facSer = fac_ser_all_field(fac_obj)

        except facility.DoesNotExist:
            self.facSer = fac_ser_one_field(fac_obj)


def get_summary_data() -> Response:
    compObj = Compressor.objects.all().first()
    ppObj = PowerPlant.objects.all().first()
    boilObj = Boiler.objects.all().first()

    compSer = FacSerData(Compressor,
                         CompSerTwoField,
                         compObj, CompSerAllField,
                         CompSerOneField)

    compSer = compSer.facSer

    ppSer = FacSerData(PowerPlant, PPSerTwoField,
                       ppObj, PPSerAllField,
                       PPSerOneField)

    ppSer = ppSer.facSer

    boilSer = FacSerData(Boiler, BoilSerTwoField,
                         boilObj, BoilSerAllField,
                         BoilSerOneField)

    boilSer = boilSer.facSer

    # try:
    #     obj = Compressor.objects.get()
    #     if obj.date is None:
    #         compSer = CompSerTwoField(compObj)
    #     else:
    #         compSer = CompressorSerializerAllField(compObj)
    #         count += 1
    # except Compressor.DoesNotExist:
    #     compSer = CompressorSerializerOneField(compObj)
    # try:
    #     obj = PowerPlant.objects.get()
    #     if obj.date is None:
    #         ppSer = PPSerTwoField(ppObj)
    #     else:
    #         ppSer = PowerPlantSerializerAllField(ppObj)
    #         count += 1
    # except PowerPlant.DoesNotExist:
    #     ppSer = PowerPlantSerializerOneField(ppObj)
    # try:
    #     obj = Boiler.objects.get()
    #     if obj.date is None:
    #
    #         boilSer = BoilSerTwoField(ppObj)
    #     else:
    #         boilSer = BoilerSerializerAllField(boilObj)
    #         count += 1
    # except Boiler.DoesNotExist:
    #     boilSer = BoilerSerializerOneField(boilObj)

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

        gasSer = GasSerAllField(gasObj)
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

    count: int = 0

    for key, value in responce.data.items():
        if key != 'gases':
            for key2, value2 in value.items():
                if (key2 == 'date') and value2:
                    count += 1
                    break
        else:
            for key2, value2 in value.items():
                for key3, value3 in value2.items():
                    if (key3 == 'date') and value3:
                        count += 1
                        break

    isConfirmable = True

    if (count != len(responce.data.keys())) or isConfirmed:
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
