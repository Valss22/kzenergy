import base64
import json


def parse_id_token(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise Exception("Incorrect id token format")

    payload = parts[1]
    padded = payload + '=' * (4 - len(payload) % 4)
    decoded = base64.b64decode(padded)
    return json.loads(decoded)


def parse_date(date: str) -> str or None:
    if date is None:
        return date
    return date.split('.')[0][:-3]


def parse_number(num: int) -> int:
    if num % 1 == 0:
        return int(num)
    else:
        return num
