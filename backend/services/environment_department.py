from rest_framework.response import Response

from backend.models import Formulas, Compressor, PowerPlant, Boiler, Gas, Archive
from backend.parsing import parse_date
from backend.serializers import FormulasSerializer, CompSerArchive, PPSerArchive, BoilSerArchive
from backend.services.auth import get_current_user
from backend.services.excel import create_excel


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
        response.data = {'archive': archive.environmentDep}
        response.data['archive']['date'] = archive.date

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

    miningDep = {
        'user': {
            'fullName': formulas.user.fullName,
            'id': formulasDict['user_id']
        },
        'date': formulasDict['date'],
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
            'NO2': round(formulasDict['NO2coef'] * density * volume * gasDict['nitrogen'], 2),
            'NO': round(formulasDict['NOcoef'] * density * volume * gasDict['nitrogen'], 2),
            'SO2': round(formulasDict['SO2coef'] * density * volume * gasDict['sulfur'], 2),
            'CO': round(formulasDict['COcoef'] * density * volume * gasDict['carbon'], 2),
            'CO2': round(gasDict['CO2EmissionFactor'] * formulasDict['CO2coef'] * density * volume * lowHeatCom, 2),
            'CH4': round(gasDict['CH4SpecificFactor'] * formulasDict['CH4coef'] * density * volume * lowHeatCom, 2),
            'N2O': round(gasDict['N2OSpecificFactor'] * formulasDict['N2Ocoef'] * density * volume * lowHeatCom, 2),
        }

    compPoll = facility_pollutants(Vcomp)
    ppPoll = facility_pollutants(Vpp)
    boilPoll = facility_pollutants(Vboil)

    compPoll['energy'] = round(Vcomp / comp.volumeOfInjectedGas, 2)
    ppPoll['energy'] = round(pp.workingHours * Vpp / pp.generatedElectricity, 2)
    boilPoll['energy'] = round(Vboil / boil.steamVolume, 2)

    def get_total_poll(facility):
        facility['totalEmis'] = sum([
            facility['NO2'], facility['NO'],
            facility['SO2'], facility['CO']
        ])

        facility['totalGrhs'] = sum([
            facility['CO2'], facility['CH4'],
            facility['N2O']
        ])

    get_total_poll(compPoll)
    get_total_poll(ppPoll)
    get_total_poll(boilPoll)

    currentUser = get_current_user(request)

    import cloudinary.uploader
    dictForExcel = get_data_for_excel()
    create_excel(**dictForExcel)
    excel = cloudinary.uploader.upload('report.xlsx', resource_type='auto')

    environmentDep = {
        'user': {
            'fullName': currentUser.fullName,
            'id': currentUser.id
        },
        'compressor': compPoll,
        'powerplant': ppPoll,
        'boiler': boilPoll,
        'excel': excel['secure_url']
    }

    import datetime

    Archive.objects.create(
        date=parse_date(str(datetime.datetime.now())),
        compressor=comSer.data,
        powerplant=ppSer.data,
        boiler=boilSer.data,
        miningDep=miningDep,
        environmentDep=environmentDep
    )

    Gas.objects.get().delete()
    Formulas.objects.filter().update(isConfirmed=False, date=None, user=None)

    return get_response_environment()
