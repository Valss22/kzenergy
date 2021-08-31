from rest_framework.response import Response

from backend.serializers import AvatarSerializer
from backend.services.auth import get_current_user
import cloudinary.uploader


def update_profile(request):
    if 'avatar' in request.data:
        return update_avatar(request)
    else:
        return update_phone(request)


def update_avatar(request):
    current_user = get_current_user(request)
    changed_avatar = cloudinary.uploader.upload(request.data['avatar']['data'])
    current_user.avatar = changed_avatar
    current_user.save()
    serializer = AvatarSerializer(current_user)
    return Response({'avatar': serializer.data['avatar']})


def update_phone(request):
    current_user = get_current_user(request)
    changed_phone = request.data['phone']
    current_user.phone = changed_phone
    current_user.save()
    return Response({'phone': current_user.phone})
