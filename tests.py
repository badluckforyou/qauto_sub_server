import os
import time
import platform
import ujson as json

from core.api.request import *
from common.helper import get_execution


if platform.system() == "Windows":
    import win32file
else:
    win32file = None


def record(data):
    file = os.path.join(get_execution(), "result.txt")
    with open(file, "w+", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    if win32file is not None:
        win32file._setmaxstdio(65535)
    payload = []
    robot_number = 2100
    django = "http://192.168.1.37:8888/login/"
    subserver = "http://192.168.1.37:8080/"
    baidu = "http://www.baidu.com"
    travel = "https://www.12306.cn/index/"
    for i in range(robot_number):
        d = {'username': "ylem",
            'password': 'bindo123',
            "remember": True}
        payload.append(d)
    # post(subserver, payload)
    result = get(baidu, robot_number)
    data = []
    for r in result:
        r["recv_data"] = ""
        data.append(r)
    record(data)