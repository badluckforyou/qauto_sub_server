import time
import platform
import traceback

from core.settings import Settings
from common.helper import run_cmd, delay_after_operation
from common.exceptions import FindError
from core.refactor.appium_refactor import AppiumRefactor


__author__ = "Jackey"


# 利用getattr来调用appium函数
iOS = {
    "element": {
        "predicate": "find_element_by_ios_predicate",
        "classchain": "find_element_by_ios_predicate",
        "uiautomation": "find_element_by_ios_uiautomation",
    },
    "elements": {
        "predicate": "find_elements_by_ios_predicate",
        "classchain": "find_elements_by_ios_predicate",
        "uiautomation": "find_elements_by_ios_uiautomation",
    },
}


class iOSAppium(AppiumRefactor):

    """appium on iOS"""

    def __init__(self, session):
        super().__init__(session, platform="ios")
        self.platform = platform
        # ios似乎杀掉ideviceslog进程可以降低Cpu消耗
        if self.platform == "ios":
            run_cmd("kill ideviceslog")

    def find_element(self, ele, method=None, one=True):
        """
        one = False, iOS查找所有符合要求的元素
        one = True,  iOS查找首个符合要求的元素
        大部分的操作都要查找元素, 所以将其写为一个通用接口
        """
        # 如果传入list, 则设置type为效率最高的predicate
        if method is None:
            method = "predicate"
        # ele必需为list且长度不能大于2
        if isinstance(ele, list):
            if len(ele) > 2: raise ValueError
        else: raise ValueError
        # 校验查找方法是否存在
        if method not in iOS["element"] and one is True:
            raise ValueError

        if method not in iOS["elements"] and one is False:
            raise ValueError

        if method == "predicate":
            # 仅有元素: "type == 'xxx' "
            # 带元素名: "type == 'xxx' AND name CONTAINS 'xxx'"
            arg = "type == '%s'" % ele[0]
            if len(ele) == 2:
                arg += " AND name CONTAINS '%s'" % ele[1]
        else:
            arg = ele[0]

        return self._find_element(method, one, arg)

    def _find_element(self, key, one, arg):
        try:
            # 每次找到后都等一下, 等待时间从Settings中获取
            delay_after_operation(Settings.find_interval)
            method = iOS["element"].get(key) if one is True else iOS["elements"].get(key)
            return getattr(self.driver, method)(arg)
        except: raise FindError   