from rest_framework.views import APIView

from backend.permissions import IsCreated, IsAuth, IsGasExists
from backend.serializers import *
from backend.services.auth import *
from backend.services.common import get_obj, OBJ_WORKER, CHEM_WORKER
from backend.services.facility import create_facility, FacilityRequest
from backend.services.gas_composition import create_gas_composition


class SignInView(APIView):

    def post(self, request):
        return sign_in(request)


class LoginView(APIView):

    def post(self, request):
        return login(request)


class FacilityView(APIView):
    permission_classes = [IsAuth, IsCreated]

    model = None
    modelSerializer = None

    @classmethod
    def get(cls, request):
        FacilityRequest(request, cls)
        return get_obj(model=cls.model, group=OBJ_WORKER,
                       modelSerializer=cls.modelSerializer)

    @classmethod
    def post(cls, request):
        path = request.get_full_path()
        FacilityRequest(request, cls)
        return create_facility(request, path,
                               cls.model, cls.modelSerializer)


class GasCompositionView(APIView):
    permission_classes = [IsAuth, IsGasExists]

    def get(self, request):
        gasName = request.query_params['gasName']

        return get_obj(gasName=gasName, model=Gas,
                       group=CHEM_WORKER,
                       modelSerializer=GasSerializer)

    def post(self, request):
        return create_gas_composition(request, Gas, GasSerializer)


class MiningDepartmentView(APIView):

    def get(self, request):
        compObj = Compressor.objects.all().first()
        ppObj = PowerPlant.objects.all().first()
        boilObj = Boiler.objects.all().first()

        compSer = CompressorSerializer3Group(compObj)
        ppSer = PowerPlantSerializer3Group(ppObj)
        boilSer = BoilerSerializer3Group(boilObj)

        gasObj = Gas.objects.all()
        gasSer = GasSerializer(gasObj, many=True)

        return Response({'compressor': compSer.data,
                         'powerPlant': ppSer.data,
                         'boiler': boilSer.data,
                         'gas': gasSer.data})
