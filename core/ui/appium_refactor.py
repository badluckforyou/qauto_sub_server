# 将appium二次开发, 使得appium自动化更好编写
# 代码主要服务于iOS端和android端的基本操作
# 两个端的核心find方法不一致, 因此该方法需要在两个端内部添加
# 由于目前主要用到的只有等、点、写、清除、滑动5个功能
# 暂时只封装这5个功能, 后续有需要再添加

import os
import time
import logging
import traceback

from appium import webdriver
from contextlib import suppress

from core.settings import Settings
from common.record import Record
from common.helper import delay_after_operation
from common.exceptions import (PlatformError, ElementError, WriteError, 
                                ClickError, SwipeError, WaitError)



__author__ = "Jackey"


LOGGER = logging.getLogger("autotest")


class AppiumRefactor:

    """重构appium相关操作模块, 使其更方便使用"""

    def __init__(self, session, platform=None):
        """
        查找元素根据不同平台调用的appium方法也不一致
        因此放到对应平台去写self.find_element()
        find_element需要通过one=True or False来控制查找单个/全部
        如果直接调用这个类来执行, 则raise platform error
        """
        if platform is None:
            raise PlatformError
        if not isinstance(session, dict):
            raise ValueError("Appium gets a wrong session: %s" % session)
        try:
            self.init_driver = webdriver.Remote("http://localhost:4723/wd/hub", session)
            self.driver = self.init_driver
        except:
            traceback.print_exc()
            raise
        self.method = None
        # 页面的全部元素
        self.page_source = self.driver.page_source

    def set_method(self, method):
        """如果想自定义查找元素的方法, 调用此方法即可"""
        self.method = method

    def clear_method(self):
        """修改默认查找方法后, 可调用此方法进行清除"""
        self.method = None

    def set_driver(self, driver):
        """在某种情况下为了查找元素可能需要重新设定driver"""
        self.driver = driver

    def reset_driver(self):
        """将driver重置为初始driver"""
        self.driver = self.init_driver

    def wait_element(self, ele, method=None, one=True, duration=None):
        """
        等待元素的出现, 自动化大部分时间所需要的元素都是必须有的, 
        所以用等待元素最为适合, 在此将等待写成一个通用的方法方便调用
        """
        # 设置查找时间, 未传入时间则从Settings中获取
        if duration is None:
            end_time = time.time() + Settings.wait_duration
        elif isinstance(duration, int) or isinstance(duration, float):
            end_time = time.time() + duration
        else: raise ValueError
        
        while True:
            with suppress(Exception):
                if method is None:
                    method = self.method
                return self.find_element(ele, method=method, one=one)
            # 设置查找间隔, 时间从Settings中获取
            delay_after_operation(Settings.wait_interval)
            # 等待时间超出一定时间, 则表明没有该元素, raise以防止资源一直被占用
            if time.time() > end_time:
                LOGGER.warning("Wait for %s timeout." % ele)
                raise WaitError

    def window_size(self):
        """获取屏幕大小"""
        window = self.driver.get_window_size()
        return window["width"], window["height"]
        
    @Record.monitor
    def find(self, ele):
        with suppress(Exception):
            return self.find_element(ele, method=self.method, one=True)

    @Record.monitor
    def find_all(self, ele):
        with suppress(Exception):
            return self.find_element(ele, method=self.method, one=False)

    @Record.monitor
    def wait(self, ele):
        try:
            return self.wait_element(ele, method=self.method, one=True)
        except: raise WaitError

    @Record.monitor
    def wait_all(self, ele):
        try:
            return self.wait_element(ele, method=self.method, one=False)
        except: raise WaitError

    @Record.monitor
    def click(self, ele, times=1):
        """查找并点击元素, 用于单个元素"""
        element = self.wait_element(ele, method=self.method, one=True)
        try:
            if element:
                # 隐藏元素需要等待直到其为可见, 最大次数从Settings中获取
                for _ in range(Settings.drag_hidden_ele_times):
                    if not element.is_displayed():
                        # 将隐藏元素拽出来, 两种方法各有优缺点
                        # click有概率直接点击到隐藏元素, 但效率高于send_keys
                        # send_keys不会点击到隐藏元素，但耗时比click多10~20s
                        with suppress(Exception):
                            element.click()
                            # element.send_keys()
                        delay_after_operation(Settings.click_interval)
                        element = self.wait_element(ele, method=self.method, one=True)
                    else:
                        break
                for _ in range(times):
                    delay_after_operation(Settings.click_interval)
                    element.click()
        except: raise ClickError

    @Record.monitor
    def click_some(self, ele, idents, times=1):
        """查找多个元素并点击指定元素"""
        elements = self.wait_element(ele, method=self.method, one=False)
        try:
            if elements:
                # 如果传入了int, 说明只需要点一个
                if isinstance(idents, int):
                    ident = idents
                    if not elements[ident].is_displayed():
                        LOGGER.warning("The element is not displayed.")
                    for _ in range(times):
                        elements[ident].click()
                # list则表明需要点多个
                elif isinstance(idents, list):
                    for ident in idents:
                        if isinstance(ident, int):
                            if not elements[ident].is_displayed():
                                LOGGER.warning("The element is not displayed.")
                            for _ in range(times):
                                elements[ident].click()
                        else: raise
                else: raise
        except: raise ClickError

    @Record.monitor
    def click_all(self, ele, times=1):
        """查找多个元素并点击全部元素"""
        elements = self.wait_element(ele, method=self.method, one=False)
        try:
            if elements:
                for element in elements:
                    if not element.is_displayed():
                        LOGGER.warning("The element is not displayed.")
                    for _ in range(times):
                        element.click()
        except: raise ClickError

    @Record.monitor
    def write(self, ele, text):
        """在元素中写入text内容, 用于单个元素"""
        element = self.wait_element(ele, method=self.method, one=True)
        if not isinstance(text, str) and not isinstance(text, int):
            raise WriteError
        try:
            if element:
                delay_after_operation(Settings.write_interval)
                element.send_keys(text)
        except: raise WriteError

    @Record.monitor
    def clear(self, ele):
        """清除元素中写入的内容, 用于单个元素"""
        element = self.wait_element(ele, method=self.method, one=True)
        try:
            if element:
                element.clear()
        except: raise ClearError

    @Record.monitor
    def swipe(self, source, target):
        """从source滑动到target
        """
        try:
            s_x, s_y = source
            t_x, t_y = target
            page_source_before = self.driver.page_source
            self.driver.swipe(s_x, s_y, t_x, t_y, Settings.swipe_duration)
            page_source_after  = self.driver.page_source
            # 判断页面是否到了最上/下/左/右
            if page_source_before == page_source_after:
                return False
            return True
        except: raise SwipeError

    def screenshot(self, filename, specified=True):
        """截图"""
        if specified is True:
            # 截图并将图片存到指定定位, filename可带路径
            self.driver.get_screenshot_as_file(filename)
        else:
            # 截图并将图片存在当前位置
            self.driver.save_screenshot(filename)
    
    def stop(self):
        self.driver.close_app()

    def start(self):
        self.driver.launch_app()

    def restart(self):
        self.close()
        delay_after_operation(0.5)
        self.start()