from rest_framework.response import Response
from rest_framework import status


# def validate_full_name(value: str) -> bool:
#     words_value = value.split(' ')
#     parsed_value = [i for i in words_value if '' != i]
#
#     if len(parsed_value) != 3:
#         return False
#     return True


def validate_role(value: str) -> bool:
    role_choices = ['роль1', 'роль2', 'роль3', 'роль4']
    if value not in role_choices:
        return False
    return True
