from backend.services.common import get_obj, create_obj, CHEM_WORKER


def get_gas_name(facility_name: str):
    if facility_name in ['compressor', 'powerPlant', 'boiler']:
        return 'sweetGas'


def update_gas_composition(request, model):
    gasComposition = model.objects.filter(gasName=request.data['gasName'])
    gasComposition.update(**request.data)


def create_gas_composition(request, model, model_serializer):

    if model.objects.filter(gasName=request.data['gasName']).exists():
        update_gas_composition(request, model)
    else:
        create_obj(request=request, model=model, group=CHEM_WORKER)

    return get_obj(gasName=request.data['gasName'], model=model,
                   modelSerializer=model_serializer, group=CHEM_WORKER)
