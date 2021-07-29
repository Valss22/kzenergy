from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from backend.data_fields import fieldsDict
from backend.models import Archive


def get_percent_deviation(facility: str, field: str, curr_value: float):
    total = 0
    archive = Archive.objects.all()

    if len(archive) > 1:
        for arch in archive:
            print(arch.__dict__['EPWorker'][facility][field])
            total += arch.__dict__['EPWorker'][facility][field]

        avg = total / len(archive)
        onePer = avg / 100
        return (curr_value - avg) / onePer

    return None


def percent_deviation(facility: str, field: str, curr_value: float) -> dict:
    return {
        field + '%': get_percent_deviation(facility, field, curr_value)
    }


def get_percent_fields(facility_poll: {str: dict}, ) -> dict:
    facilityPollPercent = {'compressor': {},
                           'powerplant': {},
                           'boiler': {}}

    # print(facility_poll.keys())

    for fName in facility_poll.keys():
        for key, value in facility_poll[fName].items():
            # print(key, type(value))
            facilityPollPercent[fName].update(percent_deviation(fName, key, value))

    print(facilityPollPercent)
    return facilityPollPercent


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
