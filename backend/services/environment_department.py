from rest_framework.response import Response

from backend.models import Formulas, Compressor, PowerPlant, Boiler, Gas
from backend.parsing import parse_date
from backend.serializers import FormulasSerializer


def get_status_environment(facilities: dict):
    responce = Response()
    responce.data = {}

    for key, value in facilities.items():
        try:
            obj = value.objects.get()
            if not obj.user:
                obj.date = parse_date(obj.date)
                responce.data[key] = f'{obj.user.fullName} {obj.date}'
            else:
                responce.data[key] = None
        except value.DoesNotExist:
            responce.data[key] = None

    return responce


def get_calculated_formulas():
    formulas = Formulas.objects.get()

    if not formulas.isConfirmed:
        facilities = {
            'compressor': Compressor,
            'powerplant': PowerPlant,
            'boiler': Boiler,
            'sweetGas': Gas
        }
        return get_status_environment(facilities)

    serializer = FormulasSerializer(formulas)
    return Response(serializer.data)


def update_formula(request):
    Formulas.objects.all().update(**request.data)
    return get_calculated_formulas()
