import datetime

from backend.parsing import parse_date
from backend.services.auth import get_current_user


def get_refusal_data(request) -> dict:
    refusalData = {'text': request.data['text']}
    date = parse_date(str(datetime.datetime.now()))
    refusalData['date'] = date
    currentUser = get_current_user(request)
    user = {'fullName': currentUser.fullName,
            'id': currentUser.id}
    refusalData['user'] = user
    return refusalData
