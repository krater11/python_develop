import base64
import os.path
import sqlite3
from settings import DATABASE,image_path


def UploadImage(image, photo_name):
    file_path = os.path.join(image_path, photo_name)
    # try:
    #     with open(file_path, "wb") as file:
    #         file.write(image)
    # except Exception:
    #     return 400, "上传失败"
    return 200, "上传成功"