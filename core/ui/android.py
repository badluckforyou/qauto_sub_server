import time
import traceback

from core.settings import Settings
from common.helper import delay_after_operation
from common.exceptions import FindError
from core.ui.appium_refactor import AppiumRefactor


__author__ = "Jackey"



# 利用getattr来调用appium函数
android = {
    "element": {
        "id": "find_element_by_id",
        "name": "find_element_by_name",
        "xpath": "find_element_by_xpath",
        "classname": "find_element_by_class_name",
        "viewtag": "find_element_by_android_viewtag",
        "accessibilityid": "find_element_by_accessibility_id",
        "wiewmatcher": "find_element_by_android_view_matcher",
        "datamatcher": "find_element_by_android_data_matcher",
        "uiautomation": "find_element_by_android_uiautomation",
    },
    "elements": {
        "id": "find_elements_by_id",
        "name": "find_elements_by_name",
        "xpath": "find_elements_by_xpath",
        "classname": "find_elements_by_class_name",
        "viewtag": "find_elements_by_android_viewtag",
        "accessibilityid": "find_elements_by_accessibility_id",
        "datamatcher": "find_elements_by_android_data_matcher",
        "uiautomation": "find_elements_by_android_uiautomation",
    },
}


class AndroidAppium(AppiumRefactor):

    """appium on android"""

    def __init__(self, session):
        super().__init__(session, platform="android")

    def find_element(self, ele, method=None, one=True):
        """
        one = False, iOS查找所有符合要求的元素
        one = True,  iOS查找首个符合要求的元素
        大部分的操作都要查找元素, 所以将其写为一个通用接口
        """
        # 如果method为None, 则设置其为默认值
        # 默认值暂定为xpath, 后续调整为效率最高的方法
        if method is None:
            method = "xpath"
        # 校验查找方法是否存在
        if method not in android["element"] and one is True:
            raise ValueError

        if method not in android["elements"] and one is False:
            raise ValueError

        return self._find_element(method, one, ele)

    def _find_element(self, key, one, arg):
        try:
            # 每次找到后都等一下, 等待时间从Settings中获取
            delay_after_operation(Settings.find_interval)
            method = android["element"].get(key) if one is True else android["elements"].get(key)
            return getattr(self.driver, method)(arg)
        except: raise FindError