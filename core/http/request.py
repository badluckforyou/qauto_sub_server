import json
import requests

from common.log import logger

def post(*args, **kwargs):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    response = requests.post(*args, headers=headers, **kwargs)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        logger.error("Status code is %s\n" % (response.status_code))


def connect_central_server(data, host, port):
    """
    连接中心服
    args:
        data: 储存用户启动sub-server时传入的username,password,single,status数据的类
        host: 本机host
        port: 默认为8080
    returns:
        central server的返回数据 or None
    """
    url = "http://192.168.191.249:8888/automation/share/"
    data = {
        "username": data.username,
        "password": data.password,
        "single": data.single,
        "status": data.status,
        "host": host,
        "port": data.port
    }
    return post(url, data=data)


def send_2_central_server_insert(data):
    """
    向中心服发送测试结果数据
    Args:
        data 须为字典且长度必须为12
    """
    if not isinstance(data, dict):
        return
    if len(data) != 12:
        return
    # cols = ["username", "project", "casename", 
    #         "runtime", "resultwanted", "resultinfact",
    #         "testresult", "costtime", "log", "report", "image"]
    # d = {}
    # for i, v in enumerate(cols):
    #     d.setdefault(v, data[i])
    url = "http://192.168.191.249:8888/result/insert/"
    return post(url, data=data)

def send_2_central_server_update(data):
    """
    向中心服发送任务状态
    """
    if not isinstance(data, dict):
        return
    if len(data) != 2:
        return
    url = "http://192.168.191.249:8888/automation/update/"
    return post(url, data=data)