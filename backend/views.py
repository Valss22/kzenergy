from rest_framework.views import APIView

from backend.permissions import IsCreated, IsAuth, IsGasExists, IsRightRole
from backend.serializers import *
from backend.services.auth import *
from backend.services.facility import create_facility, get_facility
from backend.services.gas import create_gas, get_gas
from backend.services.mining_department import get_summary_data


class SignInView(APIView):

    def post(self, request):
        return sign_in(request)


class LoginView(APIView):

    def post(self, request):
        return login(request)


# TODO: добавить мидлваре на роли, валидацию

class FacilityView(APIView):
    permission_classes = [IsAuth, IsRightRole, IsCreated]

    model = None
    modelSerializer = None

    @classmethod
    def get(cls, request):
        return get_facility(cls, request)

    @classmethod
    def post(cls, request):
        return create_facility(cls, request)


class GasCompositionView(APIView):
    permission_classes = [IsAuth, IsRightRole, IsGasExists]

    def get(self, request):
        return get_gas(request, Gas, GasSerializerAllField)

    def post(self, request):
        return create_gas(request)


class MiningDepartmentView(APIView, IsRightRole):  # TODO: добавить мидлваре
    permission_classes = [IsAuth, IsRightRole]

    def get(self, request):
        return get_summary_data()
