import base64
import json

GET_LIST = 'GET-LIST'


def parse_id_token(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise Exception("Incorrect id token format")

    payload = parts[1]
    padded = payload + '=' * (4 - len(payload) % 4)
    decoded = base64.b64decode(padded)
    return json.loads(decoded)


def parse_date(date: str, variant: str = None) -> str:
    if variant == GET_LIST:
        return date.split('+')[0]
    return date.split('.')[0][:-3]
