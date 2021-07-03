from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_full_name(value: str) -> None:
    words_value = value.split(' ')
    parsed_value = [i for i in words_value if '' != i]

    if len(parsed_value) != 3:
        raise ValidationError(
            _('%(value)s is not an full name'),
            params={'value': value},
        )


def validate_role(value: str) -> None:
    role_choices = ['роль 1', 'роль 2', 'роль 3', 'роль 4']
    if value not in role_choices:
        raise ValidationError(
            _('%(value)s is not an exists role'),
            params={'value': value},
        )
