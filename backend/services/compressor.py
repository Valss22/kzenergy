from rest_framework import status
from rest_framework.response import Response

from backend.models import Compressor
from backend.serializers import CompressorSerializer


def create_compressor(request):
    compressor = Compressor(**request.data)
    compressor.save()
    obj = Compressor.objects.first()
    serializer = CompressorSerializer(obj)
    return Response(serializer.data, status.HTTP_200_OK)
