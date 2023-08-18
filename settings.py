import os

DATABASE = "test.db"

ROOT_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

IMAGE_PATH = "/media/photo"

HOST = "0.0.0.0"

PORT = 8000

SECRET_KEY = "d8d9b07e13766a5ccfca84dd6568727c39be9e16ac174bd1af8ad91787fa56129436da4ebad4ac830b07c74633c1ced865e9668c90c838aa9323ecd66430a615"

RESPONSE_GOOD_MESSAGE = {
    "status": True,
    "error_code": 0,
    "msg": "",
    "data": ""
}

RESPONSE_BAD_MESSAGE = {
    "status": False,
    "error_code": 1,
    "msg": ""
}