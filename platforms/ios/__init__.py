import traceback

from common.record import Record
from platforms.ios.methods import *
from utils.django_communication import update_task



@Record.finish
def gg8157(id, *args):
    try:
        test = Common(id, *args)
        test.start()
    except:
        traceback.print_exc()
        data = {"id": id, "status": "空闲"}
        update_task(data)


@Record.finish
def gg8157_ta(id, *args):
    try:
        test = Common(id, *args)
        test.start()
    except:
        traceback.print_exc()
        data = {"id": id, "status": "空闲"}
        update_task(data)


@Record.finish
def k7701(id, *args):
    try:
        test = Common(id, *args)
        test.start()
    except:
        traceback.print_exc()
        data = {"id": id, "status": "空闲"}
        update_task(data)


@Record.finish
def retail_02(id, *args):
    try:
        test = Retail(id, *args)
        test.start()
    except:
        traceback.print_exc()
        data = {"id": id, "status": "空闲"}
        update_task(data)