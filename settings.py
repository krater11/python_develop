import os
import secrets

DATABASE = "test.db"

ROOT_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

FILE_PATH = "/media/photo"

HOST = "0.0.0.0"

PORT = 8000

RESPONSE_GOOD_MESSAGE = {
    "status": True,
    "error_code": 0,
    "msg": "",
    "data": {}
}

RESPONSE_BAD_MESSAGE = {
    "status": False,
    "error_code": 1,
    "msg": ""
}

MEDIA_LIST = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tif', 'tiff', 'mp3', 'wav', 'flac', 'acc', 'mpg', 'mpeg', 'mp4', 'avi', 'mov', 'wmv', 'swf']

IMAGE_LIST = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tif', 'tiff']

AUDIO_LIST = ['mp3', 'wav', 'flac', 'acc']

VIDEO_LIST = ['mpg', 'mpeg', 'mp4', 'avi', 'mov', 'wmv', 'swf']

AES_KEY = b'y\xabh3\x91\xac\xfc\x84~\x81B3\xe2\xd8.v\x1c\x85\xd3:\xd9M\xf2\x96\xd4\xcc\x06\xb3\xb3a\xb2\xbd'