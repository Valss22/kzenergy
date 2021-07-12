from backend.models import Gas, Compressor, PowerPlant, Boiler
from backend.serializers import CompressorSerializer, PowerPlantSerializer, BoilerSerializer
from backend.services.common import get_obj, create_obj, OBJ_WORKER
from backend.services.gas_composition import get_gas_name


class FacilityRequest:
    def __init__(self, request, cls):
        path = request.get_full_path()
        if path == '/object/compressor/':
            cls.model = Compressor
            cls.modelSerializer = CompressorSerializer
        elif path == '/object/powerplant/':
            cls.model = PowerPlant
            cls.modelSerializer = PowerPlantSerializer
        else:
            cls.model = Boiler
            cls.modelSerializer = BoilerSerializer


def create_facility(request, path, model, model_serializer):
    facilityName = path.split('/')[2]
    gasName = get_gas_name(facilityName)
    gasComposition = Gas.objects.get_or_create(gasName=gasName)[0]
    create_obj(request=request, model=model, gasComposition=gasComposition, group=OBJ_WORKER)
    return get_obj(model=model, modelSerializer=model_serializer, group=OBJ_WORKER)
