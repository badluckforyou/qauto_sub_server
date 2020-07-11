import json
import requests

from common.log import logger


TARGET_HOST = "192.168.1.37"


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
    url = "http://%s:8888/automation/share/" % TARGET_HOST
    data = {
        "username": data.username,
        "password": data.password,
        "single": data.single,
        "status": data.status,
        "host": host,
        "port": data.port
    }
    return post(url, data=data)


def insert_result(data):
    """
    向中心服发送测试结果数据
    Args:
        data 须为字典且长度必须为12
    """
    if not isinstance(data, dict):
        return
    if len(data) != 12:
        return
    url = "http://%s:8888/automation/result/insert/" % TARGET_HOST
    return post(url, data=data)


def update_task(data):
    """
    向中心服发送任务状态
    """
    if not isinstance(data, dict):
        return
    url = "http://%s:8888/automation/update/" % TARGET_HOST
    return post(url, data=data)