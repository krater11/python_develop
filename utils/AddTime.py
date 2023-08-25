import datetime
import time


def add_time():
    now_time = int(time.time())
    dt = datetime.datetime.fromtimestamp(now_time)
    plus_dt = dt + datetime.timedelta(weeks=1)
    expire_time = int(plus_dt.timestamp())

    return expire_time
