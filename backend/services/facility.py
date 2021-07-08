from rest_framework import status
from rest_framework.response import Response
from backend.models import GasComposition


def create_facility(request, path, model, model_serializer):
    facility_name = path.split('/')[2]
    gasComposition = GasComposition.objects.get_or_create(facilityName=facility_name)[0]
    facility = model(**request.data)
    facility.gasComposition = gasComposition
    gasComposition.save()
    facility.save()
    obj = model.objects.first()
    serializer = model_serializer(obj)
    return Response(serializer.data, status.HTTP_200_OK)
