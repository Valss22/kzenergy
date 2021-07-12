import datetime

import jwt
from rest_framework import status
from rest_framework.response import Response

from backend.models import User
from kzenergy import settings

OBJ_WORKER = 'objWorker'
CHEM_WORKER = 'chemWorker'
MINING_WORKER = 'miningWorker'
EP_WORKER = 'EPWorker'


# Получение данных из моделей в рабочей зоне определенной группы пользователя
def get_obj(**kwargs) -> Response:
    try:
        if kwargs['group'] == OBJ_WORKER:
            obj = kwargs['model'].objects.get()
        elif kwargs['group'] == CHEM_WORKER:
            obj = kwargs['model'].objects.get(gasName=kwargs['gasName'])
        else:
            raise ValueError
    except kwargs['model'].DoesNotExist:
        return Response({'date': None})

    serializer = kwargs['modelSerializer'](obj)
    return Response(serializer.data, status.HTTP_200_OK)


# Создание модели в рабочей зоне определленной группой пользователя
def create_obj(**kwargs) -> None:
    obj = kwargs['model'](**kwargs['request'].data)
    if kwargs['group'] == OBJ_WORKER:
        obj.gasComposition = kwargs['gasComposition']
        kwargs['gasComposition'].save()
    elif kwargs['group'] == CHEM_WORKER:
        obj.date = datetime.datetime.now()
    token = kwargs['request'].headers['Authorization'].split(' ')[1]
    dataToken = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms='HS256')
    currentUser = User.objects.get(email=dataToken['email'])
    obj.user = currentUser
    obj.save()
