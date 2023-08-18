import json
from settings import RESPONSE_BAD_MESSAGE


def bad_message(response_message):
    message = RESPONSE_BAD_MESSAGE
    message["msg"] = response_message
    json_message = json.dumps(message)

    return json_message
