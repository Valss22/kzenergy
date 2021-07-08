from rest_framework import status
from rest_framework.response import Response

from backend.models import Compressor, GasComposition
from backend.serializers import CompressorSerializer


def create_compressor(request):
    gasComposition = GasComposition.objects.get_or_create(facilityName='compressor')[0]
    compressor = Compressor(**request.data)
    compressor.gasComposition = gasComposition
    gasComposition.save()
    compressor.save()
    obj = Compressor.objects.first()
    serializer = CompressorSerializer(obj)
    return Response(serializer.data, status.HTTP_200_OK)
