from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from backend.parsing import parse_date
from backend.permissions import IsAuth, IsRightRole, enable_to_edit, enable_to_create, enable_to_edit_gas
from backend.serializers import CompSerArchive, PPSerArchive, BoilSerArchive

from backend.services.auth import *
from backend.services.environment_department import get_calculated_formulas, update_formula, get_data_for_excel, \
    get_status_environment, calculate_emission
from backend.services.excel import create_excel
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
    permission_classes = [IsAuth, IsRightRole]

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
        role = request.query_params['role']

        class ArchiveSerializer(ModelSerializer):
            class Meta:
                model = Archive
                fields = (role,)

            def to_representation(self, data):
                data = super().to_representation(data)
                return data[role]

        archive = Archive.objects.all()
        serializer = ArchiveSerializer(archive, many=True)

        return Response(serializer.data)
