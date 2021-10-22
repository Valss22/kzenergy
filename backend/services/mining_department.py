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
    comp_obj = Compressor.objects.all().first()
    pp_obj = PowerPlant.objects.all().first()
    boil_obj = Boiler.objects.all().first()

    comp_ser = FacSerData(
        Compressor, CompSerTwoField, comp_obj,
        CompSerAllField, CompSerOneField
    )

    comp_ser = comp_ser.facSer

    pp_ser = FacSerData(
        PowerPlant, PPSerTwoField,
        pp_obj, PPSerAllField,
        PPSerOneField
    )

    pp_ser = pp_ser.facSer

    boil_ser = FacSerData(
        Boiler, BoilSerTwoField,
        boil_obj, BoilSerAllField,
        BoilSerOneField
    )

    boil_ser = boil_ser.facSer

    gas_names = [obj.gasName for obj in Gas.objects.all()]

    gas_dict = {}

    for i in gas_names:
        gas_obj = Gas.objects.get(gasName=i)

        if not gas_obj.date:
            class GasSer(ModelSerializer):
                class Meta:
                    model = Gas
                    fields = ('date', 'refusalData')

            gas_ser = GasSer(gas_obj)
            gas_dict[i] = gas_ser.data
            continue

        gas_ser = GasSerAllField(gas_obj)
        gas_dict[i] = gas_ser.data

    if not gas_dict:
        gas_dict['sweetGas'] = {'date': None}

    user = Formulas.objects.get().user
    date = Formulas.objects.get().date
    is_confirmed = Formulas.objects.get().isConfirmed

    if user:
        user = {'fullName': user.fullName,
                'id': user.id}

    date = parse_date(date)

    responce = Response()

    responce.data = {
        'compressor': comp_ser.data,
        'powerplant': pp_ser.data,
        'boiler': boil_ser.data,
        'gases': gas_dict,
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

    is_confirmable = True

    if (count != len(responce.data.keys())) or is_confirmed:
        is_confirmable = False

    confirm_data = {
        'user': user,
        'date': date,
        'isConfirmed': is_confirmed,
        'isConfirmable': is_confirmable
    }

    responce.data['confirmData'] = confirm_data

    return responce


def sign_report(request):
    current_user = get_current_user(request)
    Formulas.objects.all().update(
        user=current_user, date=datetime.datetime.now(),
        isConfirmed=True
    )
    return get_summary_data()
