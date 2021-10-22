from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from backend.data_fields import fields_dict
from backend.models import Archive


def get_percent_deviation(facility: str, field: str, curr_value: float):
    total = 0
    archive = Archive.objects.all()

    if len(archive) > 1:
        for arch in archive:
            total += arch.__dict__['EPWorker'][facility][field]

        avg = total / len(archive)
        one_per = avg / 100
        return str(round((curr_value - avg) / one_per, 2))

    return None


def percent_deviation(facility: str, field: str, curr_value: float) -> dict:
    return {
        field + '%': get_percent_deviation
        (facility, field, curr_value)
    }


def get_percent_fields(facility_poll: {str: dict}) -> dict:
    facility_poll_percent = {
        'compressor': {},
        'powerplant': {},
        'boiler': {}
    }

    for f_name in facility_poll.keys():
        for key, value in facility_poll[f_name].items():
            facility_poll_percent[f_name].update(
                percent_deviation(f_name, key, value)
            )

    return facility_poll_percent


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
            for i in fields_dict[role]:
                data2[i] = data[role][i]
            return data2

    archive = Archive.objects.all()
    serializer = ArchiveSerializer(archive, many=True)

    return Response(serializer.data.__reversed__())
