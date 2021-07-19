from rest_framework.response import Response

from backend.models import Formulas, Compressor, PowerPlant, Boiler, Gas
from backend.parsing import parse_number
from backend.serializers import FormulasSerializer


def get_calculated_formulas():
    formulas = Formulas.objects.get()

    if not formulas.isConfirmed:
        return Response({'date': None})

    Vcomp = Compressor.objects.get().gasConsumptionVolume
    Vpp = PowerPlant.objects.get().gasConsumptionVolume
    Vboil = Boiler.objects.get().gasConsumptionVolume

    gas = Gas.objects.get()
    p = gas.density
    Nm = gas.nitrogen
    Sm = gas.sulfur
    Cm = gas.carbon

    Q = gas.LowerHeatCombustion
    CO2emiss = gas.CO2EmissionFactor
    CH4spec = gas.CH4SpecificFactor
    N2Ospec = gas.N2OSpecificFactor

    NO2coef = formulas.NO2coef
    NOcoef = formulas.NOcoef
    SO2coef = formulas.SO2coef
    COcoef = formulas.SO2coef

    compressor = {}
    powerplant = {}
    boiler = {}

    objects = [[compressor, Vcomp], [powerplant, Vpp], [boiler, Vboil]]

    keys = [['NO2', NO2coef, Nm], ['NO', NOcoef, Nm],
            ['SO2', SO2coef, Sm], ['CO', COcoef, Cm],
            ['CO2', CO2emiss, Q], ['CH4', CH4spec, Q],
            ['N2O', N2Ospec, Q]]

    p = parse_number(p)

    for o in objects:
        for k in keys:
            k[1] = parse_number(k[1])
            o[1] = parse_number(o[1])
            k[2] = parse_number(k[2])
            o[0][k[0]] = f'{k[1]} × {o[1]} × {p} × {k[2]} = {k[1] * o[1] * p * k[2]}'

    serializer = FormulasSerializer(formulas)

    responce = {
        'compressor': compressor,
        'powerplant': powerplant,
        'boiler': boiler,
    }
    responce.update(serializer.data)

    return Response(responce)


def update_formula(request):
    Formulas.objects.all().update(**request.data)
    return get_calculated_formulas()
