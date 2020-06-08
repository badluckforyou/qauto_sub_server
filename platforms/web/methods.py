# 自动化模块的编, 针对不用的项目会不一样,
# 因此后续要改为以项目或者版本分类进行控制 

from platforms.identifier import ExecutablePath



__author__ = "Jackey"


class Methods:

    """Add the methods of your project here."""

    def __init__(self):
        # 执行行为方法前先连接手机
        ExecutablePath.connect()
        self.driver = ExecutablePath.executable_path

    def exmaple_of_open_baidu(self):
        self.driver.get_url("www.baidu.com")