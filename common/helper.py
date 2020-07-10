import os
import sys
import time
import base64
import socket
import datetime
import subprocess

from contextlib import suppress

def current_time(_format):
    return datetime.datetime.now().strftime(_format)

def time_covered_bracket():
    """返回[20-04-17 01:32:39]格式的时间"""
    return datetime.datetime.now().strftime("[%y-%m-%d %X]")


def time_without_bracket():
    """返回20-04-17 01:32:39格式的时间"""
    return datetime.datetime.now().strftime("%y-%m-%d %X")


def time_with_underline():
    """返回200417_013239格式的时间"""
    return datetime.datetime.now().strftime("%y%m%d_%H%M%S")


def time_without_second():
    """返回202004170132格式的时间"""
    return datetime.datetime.now().strftime("%Y%m%d%H%M")


def time_in_hour():
    """返回01:32:39格式的时间"""
    return datetime.datetime.now().strftime("%X")


def time_without_hour():
    """返回20200417格式的时间"""
    return datetime.datetime.now().strftime("%Y%m%d")


def logpath():
    """Return log path, if it's not exists, create it."""
    logpath = os.path.join(os.path.dirname(
                            os.path.dirname(__file__)), "log")
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    return logpath


def get_automatedtesting():
    """Return automatedtesting path, if it's not exists, create it"""
    automatedtesting = os.path.join(logpath(), "automatedtesting")
    if not os.path.exists(automatedtesting):
        os.makedirs(automatedtesting)
    return automatedtesting


def get_execution():
    """Return execution path, if it's not exists, create it"""
    execution = os.path.join(logpath(), "execution")
    if not os.path.exists(execution):
        os.makedirs(execution)
    return execution


def delay_after_operation(s):
    """Use this to avoid writing lots of time.sleep in the codes"""
    time.sleep(s)


def get_localhost():
    """获取本地ip"""
    while True:
        try:
            name = socket.getfqdn(socket.gethostname())
        except:
            name = socket.gethostname()
        with suppress(Exception):
            return socket.gethostbyname(name)


def image2str(image):
    """将图片转换为str格式"""
    with open(image, "rb") as f:
        b = base64.b64encode(f.read())
        return b.decode("ascii")


def split_cmd(cmd):
    """执行指令需要拆分成list形式"""
    return cmd.split(" ") if isinstance(cmd, str) else cmd


def run_cmd(cmd):
    """subprocess执行cmd指令, 效果优于os.popen"""
    cmds = split_cmd(cmd)
    proc = subprocess.Popen(
        cmds,
        stdout=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
    )
    stdout, stderr = proc.communicate()
    if isinstance(stdout, bytes):
        stdout = stdout.decode(sys.getfilesystemencoding())
        # sys.stdout.write(stdout)
    proc.kill()
    return stdout


class FormatTime:
    """格式化时间"""

    @classmethod
    def check_format(cls, entry):
        """Check whether the entry is int or float"""
        if isinstance(entry, int):
            return entry
        elif isinstance(entry, float):
            return entry
        elif isinstance(entry, str):
            if entry.startswith(".") or entry.endswith("."):
                raise ValueError
            from collections import Counter
            counter = Counter(entry)
            try:
                if "." not in counter:
                    return int(entry)
                elif counter["."] == 1:
                    return float(entry)
            except:
                raise ValueError
        else:
            raise ValueError

    @classmethod
    def format(cls, time):
        """Format the time from seconds to others"""
        try:
            time = cls.check_format(time)
            if time < 0:
                raise ValueError("Time '%s' is smaller than 0." % time)
        except:
            raise ValueError("Format time '%s' fialed." % time)
        m, s = divmod(time, 60)
        h, m = divmod(m, 60) 
        res = [
            "%.fh" % h,
            "%.fm" % m,
            "%.1fs" % s
        ]
        if h == 0 and m == 0:
            result = res[-1]
        elif h == 0 and m != 0:
            result = "".join(res[-2:])
        else:
            result = "".join(res)
        return result


class Logger:

    LOG = list()

    @classmethod
    def error(cls, message):
        cls.LOG.append("%s ERROR %s" % (time_covered_bracket(), message))

    @classmethod
    def info(cls, message):
        cls.LOG.append("%s INFO %s" % (time_covered_bracket(), message))

    @classmethod
    def warn(cls, message):
        cls.LOG.append("%s WARNNING %s" % (time_covered_bracket(), message))

    @classmethod
    def init(cls):
        cls.LOG = list()


class G:

    test_start_time = None
    message = []
    data = []

    @classmethod
    def get_wait_time(cls, time):
        if cls.test_start_time is not None:
            return "%.4fs" % (time - cls.test_start_time)

    @classmethod
    def remind(cls, **kwargs):
        cls.data.append(kwargs)

