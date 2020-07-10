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