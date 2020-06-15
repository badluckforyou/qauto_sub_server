import time
from core.api.request import *


if __name__ == '__main__':
    # win32file._setmaxstdio(2048)
    # print(win32file._getmaxstdio())
    data = []
    robot_number = 1000
    api = "http://project_x_api.stardustworld.cn/api/v1/login/"
    for i in range(robot_number):
        d = {'identity_type': str(i),
            'identifier': 'e426cd52d8cf18f1620784f5756afff5123123213'}
        data.append(d)
    get("https://www.baidu.com", 1400)