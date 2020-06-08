import time
import traceback

from core.settings import Settings
from common.exceptions import FindError
from core.refactor.selenium_refactor import SeleniumRefactor

# 利用getattr来调用selenium函数
web = {
    "element": {
        "id": "find_element_by_id",
        "name": "find_element_by_name",
        "xpath": "find_element_by_xpath",
        "tagname": "find_element_by_tag_name",
        "linktext": "find_element_by_link_text",
        "classname": "find_element_by_class_name",
        "cssselector": "find_element_by_css_selector",
        "partiallinktext": "find_element_by_partial_link_text",
    },
    "elements": {
        "id": "find_elements_by_id",
        "name": "find_elements_by_name",
        "xpath": "find_elements_by_xpath",
        "tagname": "find_elements_by_tag_name",
        "linktext": "find_elements_by_link_text",
        "classname": "find_elements_by_class_name",
        "cssselector": "find_elements_by_css_selector",
        "partiallinktext": "find_elements_by_partial_link_text",
    }
}


class WebSelenium(SeleniumRefactor):

    """selenium on web"""

    def __init__(self, executable_path):
        super().__init__(executable_path)

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
        if method not in web["element"] and one is True:
            raise ValueError

        if method not in web["elements"] and one is False:
            raise ValueError

        return self._find_element(method, one, ele)

    def _find_element(self, key, one, arg):
        try:
            # 每次找到后都等一下, 等待时间从Settings中获取
            time.sleep(Settings.find_interval)
            method = web["element"].get(key) if one is True else web["elements"].get(key)
            return getattr(self.driver, method)(arg)
        except: raise FindError