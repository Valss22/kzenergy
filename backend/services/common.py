import datetime

from backend.parsing import parse_date
from backend.services.auth import get_current_user


def get_refusal_data(request) -> dict:
    refusal_data = {'text': request.data['text']}
    date = parse_date(str(datetime.datetime.now()))
    refusal_data['date'] = date
    current_user = get_current_user(request)
    user = {'fullName': current_user.fullName,
            'id': current_user.id}
    refusal_data['user'] = user
    return refusal_data
