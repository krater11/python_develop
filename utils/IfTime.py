import time
import datetime


def if_expire_time(expire_time):
    current_time = int(time.time())
    target_datetime = datetime.datetime.fromtimestamp(int(expire_time))
    current_datetime = datetime.datetime.fromtimestamp(current_time)
    if current_datetime >= target_datetime:
        return True
    else:
        return False
