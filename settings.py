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
    "data": ""
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

