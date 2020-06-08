import traceback

from common.record import Record
from platforms.ios.methods import *
from core.http.request import send_2_central_server_update


__author__ = "Jackey"



@Record.finish
def gg8157(app, testcase):
    test = Common(app, case)
    test.start()


@Record.finish
def gg8157_ta(app, testcase):
    test = Common(app, logpath, file, names)
    test.start()


@Record.finish
def k7701(app, testcase):
    test = Common(app, logpath, file, names)
    test.start()


@Record.finish
def retail_02(id, *args):
    try:
        test = Retail(id, *args)
        test.start()
    except:
        traceback.print_exc()
        data = {"id": id, "status": "空闲"}
        send_2_central_server_update(data)