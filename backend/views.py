import operator

from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from backend.data_fields import fieldsDict
from backend.parsing import parse_number
from backend.permissions import IsAuth, IsRightRole, enable_to_edit, enable_to_create, enable_to_edit_gas
from backend.services.archive import get_archive

from backend.services.auth import *
from backend.services.environment_department import get_calculated_formulas, update_formula, calculate_emission

from backend.services.facility import create_facility, get_facility, set_refusal_data, edit_data
from backend.services.gas import create_gas, get_gas, set_refusal_gas_data, edit_gas_data
from backend.services.mining_department import get_summary_data, sign_report


class SignInView(APIView):

    def post(self, request):
        return sign_in(request)


class LoginView(APIView):

    def post(self, request):
        return login(request)


class FacilityView(APIView):
    permission_classes = [IsAuth, IsRightRole]

    model: models.Model
    modelSerializer: models.Model

    @classmethod
    def get(cls, request):
        return get_facility(cls, request)

    @classmethod
    @enable_to_create
    def post(cls, request):
        return create_facility(cls, request)

    @classmethod
    def patch(cls, request):
        return set_refusal_data(cls, request)

    @classmethod
    @enable_to_edit
    def put(cls, request):
        return edit_data(cls, request)


class GasCompositionView(APIView):
    # permission_classes = [IsAuth, IsRightRole]

    def get(self, request):
        return get_gas(request)

    def post(self, request):
        return create_gas(request)

    def patch(self, request):
        return set_refusal_gas_data(request)

    @enable_to_edit_gas
    def put(self, request):
        return edit_gas_data(request)


class MiningDepartmentView(APIView):
    # permission_classes = [IsAuth, IsRightRole]

    def get(self, request):
        return get_summary_data()

    def patch(self, request):
        return sign_report(request)


class EnvironmentDepartmentView(APIView):
    # permission_classes = [IsAuth, IsRightRole]

    def get(self, request):
        return get_calculated_formulas()

    def patch(self, request):
        return update_formula(request)

    def post(self, request):
        return calculate_emission(request)


class ArchiveView(APIView):

    def get(self, request):
        return get_archive(request)


class MainView(APIView):

    def get(self, request):
        getParams: dict = request.query_params
        period = getParams['period']
        emis = getParams['emis']

        pollutants = ['NO2', 'NO', 'SO2', 'CO']
        grhs = ['CO2', 'CH4', 'N2O']

        massOfEmissions = {}

        def get_total_emis(facility: str) -> float:
            total = 0

            archive = Archive.objects.all()
            if period == 'last':
                archive = [archive.last()]

            i: int = 0
            for arch in archive:
                if emis == 'pollutants':
                    total += arch.__dict__['EPWorker'][facility]['totalEmis']
                    for el in pollutants:
                        v = arch.__dict__['EPWorker'][facility][el]
                        if i == 0:
                            massOfEmissions[el] = v
                        else:
                            massOfEmissions[el] += v
                elif emis == 'grhs':
                    total += arch.__dict__['EPWorker'][facility]['totalGrhs']
                    for el in grhs:
                        v = arch.__dict__['EPWorker'][facility][el]
                        if i == 0:
                            massOfEmissions[el] = v
                        else:
                            massOfEmissions[el] += v
                else:
                    total += arch.__dict__['EPWorker'][facility]['energy']
                i += 1

            for key, value in massOfEmissions.items():
                massOfEmissions[key] = parse_number(round(value / len(archive)))

            avg = total / len(archive)
            return parse_number(round(avg, 2))

        response = Response()
        response.data = {'graph1': {}}

        order = {}

        for f in ['compressor', 'powerplant', 'boiler']:
            total = get_total_emis(f)
            response.data['graph1'][f] = {'total': total}
            if emis != 'energy':
                response.data['graph1'][f]. \
                    update({'elems': [*massOfEmissions.values()]})
            order[f] = total

        sortedOrder = dict(sorted(order.items()))

        response.data['graph1'].update({'order': [*sortedOrder]})

        return response
