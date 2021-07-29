from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from backend.data_fields import fieldsDict
from backend.models import Archive


def get_percent_deviation(facility: str, field: str, curr_value: float):
    total = 0
    archive = Archive.objects.all()
    for arch in archive:
        total += arch.__dict__['EPWorker'][facility][field]

    if len(archive) > 1:
        avg = total / len(archive)
        onePer = avg / 100
        return (curr_value - avg) / onePer

    return None


def get_archive(request):
    role = request.query_params['role']

    class ArchiveSerializer(ModelSerializer):
        class Meta:
            model = Archive
            fields = (role,)

        def to_representation(self, data):
            data = super().to_representation(data)

            if role in ['mining', 'EPWorker']:
                return data[role]

            data2 = {}
            for i in fieldsDict[role]:
                data2[i] = data[role][i]
            return data2

    archive = Archive.objects.all()
    serializer = ArchiveSerializer(archive, many=True)

    return Response(serializer.data.__reversed__())
