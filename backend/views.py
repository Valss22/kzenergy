from rest_framework.views import APIView

from backend.permissions import IsCreated, IsAuth, IsGasExists, IsRightRole, EnableToEdit

from backend.services.auth import *
from backend.services.environment_department import get_calculated_formulas, update_formula
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
    permission_classes = [IsAuth, IsRightRole, IsCreated, ]

    model: models.Model
    modelSerializer: models.Model

    @classmethod
    def get(cls, request):
        return get_facility(cls, request)

    @classmethod
    def post(cls, request):
        return create_facility(cls, request)

    @classmethod
    def patch(cls, request):
        return set_refusal_data(cls, request)

    @classmethod
    def put(cls, request):
        return edit_data(cls, request)


class GasCompositionView(APIView):
    permission_classes = [IsAuth, IsRightRole, IsGasExists]

    def get(self, request):
        return get_gas(request)

    def post(self, request):
        return create_gas(request)

    def patch(self, request):
        return set_refusal_gas_data(request)

    def put(self, request):
        return edit_gas_data(request)


class MiningDepartmentView(APIView):
    #permission_classes = [IsAuth, IsRightRole]

    def get(self, request):
        return get_summary_data()

    def patch(self, request):
        return sign_report(request)


class EnvironmentDepartmentView(APIView):
    #permission_classes = [IsAuth, IsRightRole]

    def get(self, request):
        return get_calculated_formulas()

    def patch(self, request):
        return update_formula(request)
