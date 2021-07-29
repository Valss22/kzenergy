from rest_framework.response import Response

from backend.models import Formulas, Compressor, PowerPlant, Boiler, Gas, Archive
from backend.parsing import parse_date, parse_number
from backend.serializers import FormulasSerializer, CompSerArchive, PPSerArchive, BoilSerArchive, GasSerArchive
from backend.services.archive import get_percent_deviation
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
                response.data[key] = {'fullName': obj.user.fullName}
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
    formulasDict = Formulas.objects.get().__dict__
    gasDict = Gas.objects.get().__dict__

    comp = Compressor.objects.get()
    pp = PowerPlant.objects.get()
    boil = Boiler.objects.get()

    Vcomp = comp.gasConsumptionVolume
    Vpp = pp.gasConsumptionVolume
    Vboil = boil.gasConsumptionVolume

    volumes = {'comp': Vcomp, 'pp': Vpp, 'boil': Vboil}
    density = gasDict['density']

    for key in formulasDict.copy().keys():
        if 'coef' not in key:
            del formulasDict[key]

    coeffs = formulasDict

    lowerHeat = gasDict['LowerHeatCombustion']

    energyData = {
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
        'gas_dict': gasDict,
        'lower_heat': lowerHeat,
        'energy_data': energyData
    }


def get_response_environment():
    archive = Archive.objects.all().last()

    response = Response()

    if Archive.objects.all().exists():
        response.data = {'archive': archive.EPWorker}

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
    compObj = Compressor.objects.get()
    comSer = CompSerArchive(compObj)

    ppObj = PowerPlant.objects.get()
    ppSer = PPSerArchive(ppObj)

    boilObj = Boiler.objects.get()
    boilSer = BoilSerArchive(boilObj)

    formulasDict = Formulas.objects.get().__dict__
    gasDict = Gas.objects.get().__dict__

    formulas = Formulas.objects.get()

    mining = {
        'user': {
            'fullName': formulas.user.fullName,
            'id': formulasDict['user_id']
        },
        'date': parse_date(formulasDict['date']),
    }

    comp = Compressor.objects.get()
    pp = PowerPlant.objects.get()
    boil = Boiler.objects.get()

    Vcomp = comp.gasConsumptionVolume
    Vpp = pp.gasConsumptionVolume
    Vboil = boil.gasConsumptionVolume

    density = gasDict['density']

    def facility_pollutants(volume) -> dict:
        lowHeatCom = gasDict['LowerHeatCombustion']
        return {
            'NO2': parse_number(
                round(formulasDict['NO2coef'] * density * volume * gasDict['nitrogen'], 2)),
            'NO': parse_number(
                round(formulasDict['NOcoef'] * density * volume * gasDict['nitrogen'], 2)),
            'SO2': parse_number(
                round(formulasDict['SO2coef'] * density * volume * gasDict['sulfur'], 2)),
            'CO': parse_number(
                round(formulasDict['COcoef'] * density * volume * gasDict['carbon'], 2)),
            'CO2': parse_number(
                round(gasDict['CO2EmissionFactor'] * formulasDict['CO2coef'] * density * volume * lowHeatCom, 2)),
            'CH4': parse_number(
                round(gasDict['CH4SpecificFactor'] * formulasDict['CH4coef'] * density * volume * lowHeatCom, 2)),
            'N2O': parse_number(
                round(gasDict['N2OSpecificFactor'] * formulasDict['N2Ocoef'] * density * volume * lowHeatCom, 2)),
        }

    def percent_deviation(facility: str, field: str, curr_value: float) -> dict:
        return {
            field + '%': get_percent_deviation(facility, field, curr_value)
        }

    compPoll = facility_pollutants(Vcomp)
    compPollCopy = compPoll
    for key, value in compPollCopy.copy().items():
        compPoll.update(percent_deviation('compressor', key, value))

    ppPoll = facility_pollutants(Vpp)
    ppPollCopy = ppPoll
    for key, value in ppPollCopy.copy().items():
        ppPoll.update(percent_deviation('powerplant', key, value))

    boilPoll = facility_pollutants(Vboil)
    boilPollCopy = boilPoll
    for key, value in boilPollCopy.copy().items():
        boilPoll.update(percent_deviation('boiler', key, value))

    compEnergy = round(Vcomp / comp.volumeOfInjectedGas, 2)
    compPoll['energy'] = compEnergy
    compPoll.update(percent_deviation('compressor', 'energy', compEnergy))

    ppEnergy = round(pp.workingHours * Vpp / pp.generatedElectricity, 2)
    ppPoll['energy'] = ppEnergy
    ppPoll.update(percent_deviation('powerplant', 'energy', ppEnergy))

    boilEnergy = round(Vboil / boil.steamVolume, 2)
    boilPoll['energy'] = boilEnergy
    ppPoll.update(percent_deviation('boiler', 'energy', boilEnergy))

    def get_total_poll(facility, fac_name: str):
        totalEmis = round(sum([
            facility['NO2'], facility['NO'],
            facility['SO2'], facility['CO']
        ]), 2)
        facility['totalEmis'] = totalEmis
        facility.update(percent_deviation(fac_name, 'totalEmis', totalEmis))

        totalGrhs = round(sum([
            facility['CO2'], facility['CH4'],
            facility['N2O']
        ]), 2)
        facility['totalGrhs'] = totalGrhs
        facility.update(percent_deviation(fac_name, 'totalGrhs', totalGrhs))

    get_total_poll(compPoll, 'compressor')
    get_total_poll(ppPoll, 'powerplant')
    get_total_poll(boilPoll, 'boiler')

    gasObj = Gas.objects.get()
    gasSer = GasSerArchive(gasObj)

    currentUser = get_current_user(request)

    import cloudinary.uploader
    create_excel(**get_data_for_excel())
    excel = cloudinary.uploader.upload('report.xlsx', resource_type='auto')

    environment = {
        'user': {
            'fullName': currentUser.fullName,
            'id': currentUser.id
        },
        'date': parse_date(str(datetime.now())),
        'compressor': compPoll,
        'powerplant': ppPoll,
        'boiler': boilPoll,
        'excel': excel['secure_url']
    }

    Archive.objects.create(
        compressor=comSer.data,
        powerplant=ppSer.data,
        boiler=boilSer.data,
        chemical=gasSer.data,
        mining=mining,
        EPWorker=environment
    )

    Gas.objects.get().delete()
    Formulas.objects.filter().update(isConfirmed=False, date=None, user=None)

    return get_response_environment()
