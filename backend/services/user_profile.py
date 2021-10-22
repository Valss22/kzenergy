from rest_framework import status
from rest_framework.response import Response

from backend.models import User
from backend.serializers import AvatarSerializer, AllUsersSerializer
from backend.services.auth import get_current_user

from kzenergy.settings import PRE_URL


def update_avatar(request):
    current_user = get_current_user(request)
    changed_avatar = request.data['avatar']
    current_user.avatar = changed_avatar
    current_user.save()
    serializer = AvatarSerializer(current_user)
    return Response({'avatar': PRE_URL + serializer.data['avatar']})


def update_phone(request):
    current_user = get_current_user(request)
    changed_phone = request.data['phone']
    current_user.phone = changed_phone
    current_user.save()
    return Response({'phone': current_user.phone})


def get_users(request, pk):
    if pk:
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'user does not exist'},
                            status.HTTP_400_BAD_REQUEST)

        serializer = AllUsersSerializer(user)
        return Response(serializer.data)

    current_user = get_current_user(request)
    queryset = User.objects.exclude(email=current_user.email)
    serializer = AllUsersSerializer(queryset, many=True)
    return Response(serializer.data)
