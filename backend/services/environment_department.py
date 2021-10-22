from rest_framework.response import Response

from backend.models import Formulas, Compressor, PowerPlant, Boiler, Gas, Archive
from backend.parsing import parse_date, parse_number
from backend.serializers import FormulasSerializer, CompSerArchive, PPSerArchive, BoilSerArchive, GasSerArchive
from backend.services.archive import get_percent_deviation, get_percent_fields
from backend.services.auth import get_current_user
from backend.services.excel import create_excel
from datetime import datetime


def get_status_environment(facilities: dict):
    response = Response()
    response.data = {}

    for key, value in facilities.items():
        try:
            obj = value.objects.get()
            if obj.user:
                obj.date = parse_date(obj.date)
                response.data[key] = {'fullName': obj.user.fullName,
                                      'id': obj.user.id}
                response.data[key]['date'] = obj.date
            else:
                response.data[key] = None
        except value.DoesNotExist:
            response.data[key] = None

    return response


def get_calculated_formulas():
    formulas = Formulas.objects.get()

    if not formulas.isConfirmed:
        return get_response_environment()

    serializer = FormulasSerializer(formulas)
    return Response(serializer.data)


def update_formula(request):
    Formulas.objects.all().update(**request.data)
    return get_calculated_formulas()


def get_data_for_excel() -> dict:
    formulas_dict = Formulas.objects.get().__dict__
    gas_dict = Gas.objects.get().__dict__

    comp = Compressor.objects.get()
    pp = PowerPlant.objects.get()
    boil = Boiler.objects.get()

    Vcomp = comp.gasConsumptionVolume
    Vpp = pp.gasConsumptionVolume
    Vboil = boil.gasConsumptionVolume

    volumes = {'comp': Vcomp, 'pp': Vpp, 'boil': Vboil}
    density = gas_dict['density']

    for key in formulas_dict.copy().keys():
        if 'coef' not in key:
            del formulas_dict[key]

    coeffs = formulas_dict

    lower_heat = gas_dict['LowerHeatCombustion']

    energy_data = {
        'comp': {'hours': comp.workingHours,
                 'volumeOfInjected': comp.volumeOfInjectedGas},
        'pp': {'hours': pp.workingHours,
               'generatedEnergy': pp.generatedElectricity},
        'boil': {'hours': boil.workingHours,
                 'volumeOfSteam': boil.steamVolume}
    }

    return {
        'volumes': volumes,
        'density': density,
        'coeffs': coeffs,
        'gas_dict': gas_dict,
        'lower_heat': lower_heat,
        'energy_data': energy_data
    }


def get_response_environment():
    archive = Archive.objects.all().last()
    response = Response()

    if Archive.objects.all().exists():
        response.data = {'archive': archive.EPWorker}
        facility_poll: dict = {}

        for key, value in archive.EPWorker.items():

            if key in ['compressor', 'powerplant', 'boiler']:
                facility_poll.update({key: value})

        fac_poll = get_percent_fields(facility_poll)
        for key, value in fac_poll.items():
            response.data['archive'][key].update(value)

    else:
        response.data = {'archive': None}

    facilities = {
        'compressor': Compressor,
        'powerplant': PowerPlant,
        'boiler': Boiler,
        'sweetGas': Gas
    }
    response.data['status'] = get_status_environment(facilities).data

    return response


def calculate_emission(request):
    comp_obj = Compressor.objects.get()
    com_ser = CompSerArchive(comp_obj)

    pp_obj = PowerPlant.objects.get()
    pp_ser = PPSerArchive(pp_obj)

    boil_obj = Boiler.objects.get()
    boil_ser = BoilSerArchive(boil_obj)

    formulas_dict = Formulas.objects.get().__dict__
    gas_dict = Gas.objects.get().__dict__

    formulas = Formulas.objects.get()

    mining = {
        'user': {
            'fullName': formulas.user.fullName,
            'id': formulas_dict['user_id']
        },
        'date': parse_date(formulas_dict['date']),
    }

    comp = Compressor.objects.get()
    pp = PowerPlant.objects.get()
    boil = Boiler.objects.get()

    Vcomp = comp.gasConsumptionVolume
    Vpp = pp.gasConsumptionVolume
    Vboil = boil.gasConsumptionVolume

    density = gas_dict['density']

    def facility_pollutants(volume) -> dict:
        lowHeatCom = gas_dict['LowerHeatCombustion']
        return {
            'NO2': parse_number(
                round(formulas_dict['NO2coef'] * density * volume * gas_dict['nitrogen'], 2)),
            'NO': parse_number(
                round(formulas_dict['NOcoef'] * density * volume * gas_dict['nitrogen'], 2)),
            'SO2': parse_number(
                round(formulas_dict['SO2coef'] * density * volume * gas_dict['sulfur'], 2)),
            'CO': parse_number(
                round(formulas_dict['COcoef'] * density * volume * gas_dict['carbon'], 2)),
            'CO2': parse_number(
                round(gas_dict['CO2EmissionFactor'] * formulas_dict['CO2coef'] * density * volume * lowHeatCom, 2)),
            'CH4': parse_number(
                round(gas_dict['CH4SpecificFactor'] * formulas_dict['CH4coef'] * density * volume * lowHeatCom, 2)),
            'N2O': parse_number(
                round(gas_dict['N2OSpecificFactor'] * formulas_dict['N2Ocoef'] * density * volume * lowHeatCom, 2)),
        }

    comp_poll = facility_pollutants(Vcomp)

    pp_poll = facility_pollutants(Vpp)

    boil_poll = facility_pollutants(Vboil)

    comp_energy = round(Vcomp / comp.volumeOfInjectedGas, 2)
    comp_poll['energy'] = comp_energy

    pp_energy = round(pp.workingHours * Vpp / pp.generatedElectricity, 2)
    pp_poll['energy'] = pp_energy

    boil_energy = round(Vboil / boil.steamVolume, 2)
    boil_poll['energy'] = boil_energy

    def get_total_poll(facility):
        total_emis = round(sum([
            facility['NO2'], facility['NO'],
            facility['SO2'], facility['CO']
        ]), 2)
        facility['totalEmis'] = total_emis

        total_grhs = round(sum([
            facility['CO2'], facility['CH4'],
            facility['N2O']
        ]), 2)
        facility['totalGrhs'] = total_grhs

    get_total_poll(comp_poll)
    get_total_poll(pp_poll)
    get_total_poll(boil_poll)

    gas_obj = Gas.objects.get()
    gas_ser = GasSerArchive(gas_obj)

    current_user = get_current_user(request)

    import cloudinary.uploader
    create_excel(**get_data_for_excel())
    excel = cloudinary.uploader.\
        upload('report.xlsx', resource_type='auto')

    environment = {
        'user': {
            'fullName': current_user.fullName,
            'id': current_user.id
        },
        'date': parse_date(str(datetime.now())),
        'compressor': comp_poll,
        'powerplant': pp_poll,
        'boiler': boil_poll,
        'excel': excel['secure_url']
    }

    Archive.objects.create(
        compressor=com_ser.data,
        powerplant=pp_ser.data,
        boiler=boil_ser.data,
        chemical=gas_ser.data,
        mining=mining,
        EPWorker=environment
    )

    Gas.objects.get().delete()
    Formulas.objects.filter()\
        .update(
        isConfirmed=False,
        date=None, user=None
    )

    return get_response_environment()
