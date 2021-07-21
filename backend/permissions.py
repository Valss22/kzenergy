import jwt
from rest_framework.permissions import BasePermission
from backend.models import Compressor, PowerPlant, Boiler, Gas, User
from kzenergy import settings


class IsAuth(BasePermission):
    def has_permission(self, request, view) -> bool:
        try:
            token = request.headers['Authorization'].split(' ')[1]
            jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
            return True
        except:  # TODO отрегулировать перехват
            return False


class IsRightRole(BasePermission):
    def has_permission(self, request, view) -> bool:
        path = request.get_full_path()
        roleName = path.split('/')[-2]

        token = request.headers['Authorization'].split(' ')[1]
        dataToken = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
        currentUser = User.objects.get(email=dataToken['email'])

        if request.method == 'PATCH':
            if (roleName == currentUser.role) or \
                    (currentUser.role == 'mining'):
                return True
        else:
            if roleName == currentUser.role:
                return True


def model_for_path(request):
    path = request.get_full_path()
    if path == '/object/compressor/':
        model = Compressor
    elif path == '/object/powerplant/':
        model = PowerPlant
    else:
        model = Boiler

    return model


class EnableToEdit(BasePermission):

    def has_permission(self, request, view):

        # if request.method == 'PUT':
        #     model = model_for_path(request)
        #     if not model.date:
        #         return True
        return False


class IsCreated(BasePermission):

    def has_permission(self, request, view) -> bool:

        if request.method == 'POST':
            path = request.get_full_path()

            if path == '/object/compressor/':
                model = Compressor
            elif path == '/object/powerplant/':
                model = PowerPlant
            else:
                model = Boiler

            if len(model.objects.all()) == 0:
                return True

        return True


class IsGasExists(BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.method == 'POST':

            try:
                gas = Gas.objects.get(gasName=request.data['gasName'])
                if gas.date is not None:
                    return False
                return True
            except Gas.DoesNotExist:
                return True
        return True
