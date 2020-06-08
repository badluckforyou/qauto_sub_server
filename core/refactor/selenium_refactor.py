# 将selenium二次开发, 使得selenium自动化更好编写
# 代码主要服务于web端的自动化
# selenium核心的find方法在web端内容添加

import traceback

from selenium import webdriver
from contextlib import suppress

from core.settings import Settings
from common.record import Record
from common.exceptions import OpenUrlError, WriteError, ClickError, WaitError



__author__ = "Jackey"



class SeleniumRefactor:
    
    def __init__(self, executable_path):
        try:
            # The executable_path is the file path of chromedriver,
            # download url: http://chromedriver.storage.googleapis.com/index.html
            self.driver = webdriver.Chrome(executable_path=executable_path)
        except:
            traceback.print_exc()
            raise
        self.method = None

    def set_method(self, method):
        self.method = method

    def clear_method(self):
        self.method = None

    def wait_element(self, ele, method=None, one=True, duration=None):
        """等待元素的出现"""
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
                return self.find_element(ele, method=self.method, one=one)
            # 设置查找间隔, 时间从Settings中获取
            time.sleep(Settings.wait_interval)
            if time.time() > end_time:
                break   

    @Record.monitor
    def open_url(self, url):
        """跳转到url"""
        try:
            self.driver.get(url)
        except: raise OpenUrlError

    @Record.monitor
    def maximize(self):
        """chrome窗口最大化"""
        self.driver.maximize_window()

    @Record.monitor
    def refresh(self):
        """刷新html页面"""
        self.driver.refresh()

    @Record.monitor
    def find(self, ele):
        return self.find_element(ele, method=self.method, one=True)

    @Record.monitor
    def find_all(self, ele):
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
            for _ in range(times):
                element.click()
        except: raise ClickError

    @Record.monitor
    def click_some(self, ele, idents):
        """查找多个元素并点击指定元素"""
        elements = self.wait_element(ele, method=self.method, one=False)
        try:
            if isinstance(idents, int):
                ident = idents
                for _ in range(times):
                    elements[ident].click()
            elif isinstance(idents, list):
                for ident in idents:
                    if isinstance(ident, int):
                        for _ in range(times):
                            elements[ident].click()
                    else: raise
            else: raise
        except: raise ClickError

    @Record.monitor
    def click_all(self, ele):
        """查找多个元素并点击全部元素"""
        elements = self.wait_element(ele, method=self.method, one=False)
        try:
            for element in elements:
                for _ in range(times):
                    element.click()
        except: raise ClickError

    @Record.monitor
    def write(self, ele, text):
        """在元素中写入text内容"""
        element = self.wait_element(ele, method=self.method, one=True)
        if not isinstance(text, str) and not isinstance(text, int):
            raise WriteError
        try:
            time.sleep(Settings.write_interval)
            element.send_keys(text)
        except: raise WriteError

    @Record.monitor
    def clear(self, ele):
        """清除元素中写入的内容"""
        element = self.wait_element(ele, method=self.method, one=True)
        try:
            element.clear()
        except: raise ClearError

    @Record.monitor
    def drag(self, ele, source, target):
        """将元素从source拖动到target"""
        element = self.wait_element(ele, method=self.method, one=True)
        pass