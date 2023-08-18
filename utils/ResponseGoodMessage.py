import json
from settings import RESPONSE_GOOD_MESSAGE


def login_good_message(response_message, auth_token):
    message = RESPONSE_GOOD_MESSAGE
    message["msg"] = response_message
    message["data"] = {"auth_token": auth_token}
    json_message = json.dumps(message)

    return json_message


def normal_good_message(response_message):
    message = RESPONSE_GOOD_MESSAGE
    message["msg"] = response_message
    json_message = json.dumps(message)

    return json_message


def data_good_message(response_message, data_name, data):
    message = RESPONSE_GOOD_MESSAGE
    message["msg"] = response_message
    message["data"] = {data_name: data}
    json_message = json.dumps(message)

    return json_message