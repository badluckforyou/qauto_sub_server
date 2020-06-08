import sys
import getpass

from argparse import ArgumentParser

from common.log import logger
from core.http.server import http_server_start



class Management:
 
    """
    指令解析, 用以解析manage.py启动时携带的指令
    """
    # 获取platforms目录下的文件
    def __init__(self, argv):
        self.argv = argv

    def parse_argument(self, argument, key):
        """Split argument base on key"""
        return argument.split(key)[-1]

    def execute(self):
        """
        解析argv
        -u: username
        -p: password
        -s: single, do not share my device to others
        """
        parser = ArgumentParser()
        options, args = parser.parse_known_args(self.argv)
        self.port = None
        for arg in args:
            # -u, 用户名的标识, 如果未传入用户名, 直接返回
            if "-u" in arg:
                self.username = self.parse_argument(arg, "-u")
                if not self.username:
                    sys.stderr.write("Parse username failed.\n")
                    return
            # -p, 密码的标识, 如果用户未传入密码, 将会要求其一直输入密码
            elif "-p" in arg:
                self.password = self.parse_argument(arg, "-p")
                while not self.password:
                    self.password = getpass.getpass()
                    if self.password.strip() == "":
                        sys.stderr.write("Blank passwords aren't allowed.\n")
                        self.password = ""
            # -t, 端口的标识, 如果用户未传入port, 则默认port为8080
            elif "-t" in arg:
                self.port = self.parse_argument(arg, "-t")
                if not self.port:
                    self.port = 8080 
                    sys.stdout.write("Parse port failed, set port 8080.\n")
                else:
                    self.port = int(self.port)
            
        class User:
            username = self.username
            password = self.password
            port = self.port or 8080
            # 0分享 1不分享 -s不存在则表时, 表明与他人分享自己的测试设备
            single = 0 if "-s" not in args else 1
            # 0未使用 1使用中 启动子服务器时, 将其状态设置为不在使用中
            status = 0

        http_server_start(User)


def execute_from_command_line(argv):
    management = Management(argv)
    management.execute()