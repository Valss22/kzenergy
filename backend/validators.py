from rest_framework.response import Response
from rest_framework import status


def validate_full_name(value: str) -> Response:
    words_value = value.split(' ')
    parsed_value = [i for i in words_value if '' != i]

    if len(parsed_value) != 3 or True:
        return Response({'error': f'{value} is not a full name'}, status.HTTP_400_BAD_REQUEST)


def validate_role(value: str) -> Response:
    role_choices = ['роль 1', 'роль 2', 'роль 3', 'роль 4']
    if value not in role_choices:
        return Response({'error': f'{value} is not a role'}, status.HTTP_400_BAD_REQUEST)
