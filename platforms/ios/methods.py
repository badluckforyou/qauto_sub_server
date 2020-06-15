# 自动化模块的编, 针对不用的项目会不一样,
# 因此后续要改为以项目或者版本分类进行控制 
# 现有的AutoTestMethods中的非__init__类, 均为服务于bindo pos的例子代码
# 如果想编写属于自己的框架, 可参照例子代码进行修改
import os
import time
import json

from difflib import get_close_matches

from common.csv import Csv
from common.helper import (time_without_second, time_without_bracket, current_time,
                            delay_after_operation, image2str, FormatTime, Logger, get_automatedtesting)
from core.http.request import send_2_central_server_insert, send_2_central_server_update
from platforms.identifier import iOSSession


__all__ = ("Common", "Retail")


def strip_space(data, kwall=False):
    return data.lstrip(" ").rstrip(" ") if kwall is False else data.replace(" ")

def check_food(f):
    special_foods = ["美國有骨肉眼扒(40安士)", "Sirloin 10oz", "午室套餐"]
    for food in special_foods:
        if f in food:
            return food


class Automation:

    def __init__(self, id, username, project, package, testcase):
        # 执行前先连接手机
        iOSSession.connect()
        self.driver = iOSSession.DRIVER
        if self.driver is None:
            raise ConnectionError
        self.id = id
        self.username = username
        self.project = project
        self.steps = testcase

    def find_by_text(self, text):
        return self.driver.wait(["XCUIElementTypeStaticText", text])

    def find_by_button(self, name):
        return self.driver.wait(["XCUIElementTypeButton", name])

    def find_by_field(self, name):
        return self.driver.wait(["XCUIElementTypeSearchField", name])

    def wait_by_text(self, text):
        return self.driver.wait(["XCUIElementTypeStaticText", text])

    def wait_by_button(self, name):
        return self.driver.wait(["XCUIElementTypeButton", name])

    def click_by_text(self, text, times=1):
        self.driver.click(["XCUIElementTypeStaticText", text], times=times)

    def click_by_button(self, name, times=1):
        self.driver.click(["XCUIElementTypeButton", name], times=times)

    def write_by_field(self, name, text):
        self.driver.clear(["XCUIElementTypeSearchField", name], delay=1)
        self.driver.write(["XCUIElementTypeSearchField", name], text)


class Common(Automation):

    """Add the methods of your project here."""

    def __init__(self, *args):
        super().__init__(*args)

    def start(self):
        logpath = os.path.join(self.filepath, "log")
        self.csv = Csv(os.path.join(logpath, self.logname))
        # 生成报告
        self.csv.generate(self.titles)
        for args in self.steps:
            self.log_data = list()
            start_time = time.time()
            self.log_data.append(args[0])
            now = time_in_hour()
            self.log_data.append(now)
            self.add_coustomer(strip_space(args[1]))
            self.choose_discount(strip_space(args[2]))
            # 有可能会要多次执行选择菜单再选择商品
            for arg in args[3:]:
                if arg.replace(".", "").replace(" ", "").isdigit():
                    self.get_result(strip_space(arg), start_time)
                else:
                    self.add_foods(strip_space(arg))
            self.click_by_text("Discard")
            self.click_by_button("Discard")
            self.log_data.append(FormatTime.format(time.time() - start_time))
            logname = "%s.txt" % now.replace(":", "")
            self.log_data.append(logname)
            # 将数据写入报告中
            self.csv.write(self.log_data)

            with open(os.path.join(logpath, logname), "a+") as f:
                for log in Logger.LOG:
                    f.write(log)
            Logger.init()

    def add_coustomer(self, data):
        """选择顾客"""
        i, v = data.split("&")
        self.click_by_text(i)
        self.click_by_button("Choose Customer")
        self.write_by_field("Search", v)
        delay_after_operation(3)
        self.click_by_text("Customer Code")
        self.click_by_text("PASS")
        self.click_by_text("Discount")

    def choose_discount(self, data):
        for d in data.split("&"):
            self.click_by_text(d)
        self.click_by_button("Done")

    def add_foods(self, data):
        """添加食物"""
        menu, child_munu, *foods = data.split("&")
        self.click_by_text(menu)
        self.click_by_text(child_munu)
        menu_driver = self.driver.wait(["XCUIElementTypeCollectionView", "Menu - %s" % menu])
        for food in foods:
            self.driver.set_driver(menu_driver)
            food = food.split("*")
            if len(food) == 1:
                f = food[0]
                n = 1
            elif len(food) == 2:
                f, n = food
                n = int(n)
            else:
                raise ValueError("Case Error: %s" % foods)
            if check_food(f):
                ele = None
                while not ele:
                    ele = self.find_by_text(f)
                for _ in range(n):
                    self.driver.reset_driver()
                    ele.click()
                    self.click_by_button("Done")
                    self.driver.set_driver(menu_driver)
            else:
                ele = self.find_by_text(f)
                while not ele:
                    ele = self.find_by_text(f)
                for _ in range(n):
                    ele.click()
            self.driver.reset_driver()

    def get_result(self, data, start_time):
        use_time = time.time() - start_time
        if 100 > use_time > 60:
            delay_after_operation(5)
        elif 300 > use_time >= 100:
            delay_after_operation(10)
        elif 500 > use_time >= 300:
            delay_after_operation(15)
        elif 1000 > use_time >= 500:
            delay_after_operation(30)
        elif use_time >= 1000:
            delay_after_operation(60)
        ele = self.find_by_text("HK$")
        image_name = "%s.jpg" % time_without_second()
        filename = os.path.join(self.filepath, "log", image_name)
        if ele:
            price_true = float(ele.text.split("$")[-1].replace(",", ""))
            price_want = float(data)
            self.log_data.append("$%s" % price_want)
            self.log_data.append("$%s" % price_true)
            result = "通过" if price_true == price_want else "失败"
            self.log_data.append(result)
            self.driver.screenshot(filename)
            self.log_data.append(image_name)
        else:
            self.driver.screenshot(filename)
            raise ValueError("Can't Find 'HK$' element.")



class Retail(Automation):

    def __init__(self, *args):
        super().__init__(*args)

    def start(self):
        self.discard = self.find_by_text("Discard")
        self.date = current_time("%y-%m-%d %H%M%S")
        csv = Csv("RetailTestCasesBatch5.csv")
        for args in self.steps:
            self.log = list()
            self.result = dict()
            self.result.setdefault("date", self.date)
            self.result.setdefault("username", self.username)
            self.result.setdefault("project", self.project)
            self.result.setdefault("casename", args[0])
            self.log.append(args[0])
            start_time = time.time()
            now = time_without_bracket()
            self.result.setdefault("runtime", now)
            self.log.append(now)
            if args[1]:
                self.add_coustomer(args[1])
            if args[2]:
                self.choose_discount(args[2])
            self.click_by_text("Bindo")
            if args[3]:
                self.click_by_text(args[3])
            self.add_goods(args[4])
            self.get_result(args[5], start_time)
            self.discard.click()
            delay_after_operation(0.1)
            self.find_by_button("Discard").click()
            self.result.setdefault("costtime", FormatTime.format(time.time() - start_time))
            self.log.append(FormatTime.format(time.time() - start_time))
            self.result.setdefault("log", json.dumps("\r".join(Logger.LOG)))
            self.result.setdefault("report", json.dumps("\r".join(args)))
            self.result.setdefault("image", image2str(self.image))
            os.remove(self.image)
            Logger.init()
            send_2_central_server_insert(self.result)
            csv.write(self.log)
        data = {"id": self.id, "status": "完成"}
        send_2_central_server_update(data)

    def add_coustomer(self, data):
        """选择顾客"""
        self.click_by_button("Choose Customer")
        self.write_by_field("Search", data)
        delay_after_operation(1.5)
        while True:
            ele = self.find_by_text(data)
            # ele = self.find_by_text("Customer Code")
            if ele:
                ele.click()
                break

    def choose_discount(self, data):
        self.click_by_text("PASS")
        self.click_by_text("Discount")
        self.click_by_text(data)
        self.click_by_button("Done")

    def add_goods(self, goods):
        goods = goods.split("&")
        for good in goods:
            good = good.split("*")
            if len(good) == 1:
                f = good[0]
                n = 1
            elif len(good) == 2:
                f, n = good
                n = int(n)
            else:
                raise ValueError("Case Error: %s" % goods)
            while True:
                ele = self.find_by_text(f)
                if ele:
                    for _ in range(n):
                        ele.click()
                    break

    def get_result(self, data, start_time):
        use_time = time.time() - start_time
        if 500 > use_time >= 300:
            delay_after_operation(15)
        elif 1000 > use_time >= 500:
            delay_after_operation(30)
        elif use_time >= 1000:
            delay_after_operation(60)
        imagepath = get_automatedtesting()
        image_name = "%s.png" % time_without_second()
        self.image = os.path.join(imagepath, image_name)
        delay_after_operation(1)
        ele = self.find_by_text("HK$")
        if ele:
            price_true = float(ele.text.split("$")[-1].replace(",", ""))
            price_want = float(data)
            self.result.setdefault("resultwanted", "$%s" % price_want)
            self.result.setdefault("resultinfact", "$%s" % price_true)
            self.log.append("%s/%s" % (price_want, price_true))
            self.log.append("测试通过" if price_true == price_want else "价格不符")
            result = "通过" if price_true == price_want else "失败"
            self.result.setdefault("testresult", result)
            self.driver.screenshot(self.image)
        else:
            # self.driver.screenshot(filename)
            raise ValueError("Can't Find 'HK$' element.")



class Retail2(Automation):

    def __init__(self, *args):
        super().__init__(*args)

    def start(self):
        logpath = os.path.join(self.filepath, "log")
        self.csv = Csv(os.path.join(logpath, "%s.csv" % time_without_second()))
        # 生成报告
        self.csv.generate(self.titles)
        self.find_by_button("search")
        for args in self.steps:
            self.log_data = list()
            start_time = time.time()
            self.log_data.append(args[0])
            now = time_in_hour()
            self.log_data.append(now)
            self.search_goods(args[1])
            self.click_by_text("Cancel")
            self.get_result(args[2])
            self.click_by_text("Discard")
            self.click_by_button("Discard")
            self.log_data.append(FormatTime.format(time.time() - start_time))
            logname = "%s.txt" % now.replace(":", "")
            self.log_data.append(logname)
            # 将数据写入报告中
            self.csv.write(self.log_data)

            with open(os.path.join(logpath, logname), "a+") as f:
                for log in Logger.LOG:
                    f.write(log)
            Logger.init()

    def search_goods(self, goods):
        goods = goods.split("&")
        for good in goods:
            good = good.split("*")
            if len(good) == 1:
                f = good[0]
                n = 1
            elif len(good) == 2:
                f, n = good
                n = int(n)
            else:
                raise ValueError("Case Error: %s" % goods)
            self.write_by_field("Search", f)
            ele = None
            while not ele:
                ele = self.find_by_text(f)
            for _ in range(n):
                ele.click()

    def get_result(self, data):
        ele = self.find_by_text("HK$")
        image_name = "%s.png" % time_without_second()
        self.filename = os.path.join("log", image_name)
        if ele:
            price_true = float(ele.text.split("$")[-1].replace(",", ""))
            price_want = float(data)
            self.log_data.append("$%s" % price_want)
            self.log_data.append("$%s" % price_true)
            result = "通过" if price_true == price_want else "失败"
            self.log_data.append(result)
            self.driver.screenshot(filename)
            self.log_data.append(image_name)
        else:
            self.driver.screenshot(filename)
            raise ValueError("Can't Find 'HK$' element.")



