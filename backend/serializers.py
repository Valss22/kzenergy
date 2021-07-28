from rest_framework.serializers import ModelSerializer
from backend.models import *
from backend.parsing import parse_date, parse_number


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('excel',)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('fullName', 'id')


class FacilitySerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    def to_representation(self, data):
        data = super().to_representation(data)
        data['date'] = parse_date(data['date'])
        return data


class GasSerAllField(FacilitySerializer):
    class Meta:
        model = Gas
        fields = '__all__'


class GasSerOneField(ModelSerializer):
    class Meta:
        model = Gas
        fields = ('gasName',)


class CompSerAllField(FacilitySerializer):
    gasComposition = GasSerOneField(read_only=True)

    class Meta:
        model = Compressor
        fields = '__all__'


class CompSerOneField(FacilitySerializer):
    class Meta:
        model = Compressor
        fields = ('date',)


class CompSerArchive(FacilitySerializer):
    class Meta:
        model = Compressor
        exclude = ('gasComposition', 'refusalData', 'isEdited')


class PPSerAllField(FacilitySerializer):
    gasComposition = GasSerOneField(read_only=True)

    class Meta:
        model = PowerPlant
        fields = '__all__'


class PPSerOneField(FacilitySerializer):
    class Meta:
        model = PowerPlant
        fields = ('date',)


class PPSerArchive(FacilitySerializer):
    class Meta:
        model = PowerPlant
        exclude = ('gasComposition', 'refusalData', 'isEdited')


class BoilSerAllField(FacilitySerializer):
    gasComposition = GasSerOneField(read_only=True)

    class Meta:
        model = Boiler
        fields = '__all__'


class BoilSerOneField(FacilitySerializer):
    class Meta:
        model = Boiler
        fields = ('date',)


class BoilSerArchive(FacilitySerializer):
    class Meta:
        model = Boiler
        exclude = ('gasComposition', 'refusalData', 'isEdited')


class CompSerTwoField(ModelSerializer):
    class Meta:
        model = Compressor
        fields = ('date', 'refusalData')


class PPSerTwoField(ModelSerializer):
    class Meta:
        model = PowerPlant
        fields = ('date', 'refusalData')


class BoilSerTwoField(ModelSerializer):
    class Meta:
        model = Boiler
        fields = ('date', 'refusalData')


class FormulasSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Formulas
        fields = '__all__'

    def to_representation(self, data):
        data = super().to_representation(data)
        data['date'] = parse_date(data['date'])

        for key, value in data.items():
            if 'coef' in key:
                data[key] = str(parse_number(value))

        return data


class GasSerArchive(FacilitySerializer):
    class Meta:
        model = Gas
        exclude = ('refusalData', 'isEdited')
