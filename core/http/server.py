import re
import ujson as json
import socket
import threading
import traceback

from queue import Queue
from contextlib import suppress
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
# from http.server import BaseHTTPRequestHandler

from common.log import logger
from common.helper import run_cmd, get_localhost, delay_after_operation
from core.http.monitoring import monitoring
from core.http.request import connect_central_server



def qauto(environ, start_response):
    result = monitoring(environ)
    with suppress(AssertionError):
        start_response("200", [("Content-Type", "text/html")])
    return result
    

# class WSGIServer(WSGIServer):

#     request_queue_size = 10

#     def __init__(self, *args, ipv6=False, allow_reuse_address=True, **kwargs):
#         if ipv6:
#             self.address_family = socket.AF_INET6
#         self.allow_reuse_address = allow_reuse_address
#         super().__init__(*args, **kwargs)


def release_port(port):
    stdout = run_cmd(["lsof", "-i", ":%s" % port])
    pattern = re.compile(r"\d+")
    pid = None
    for line in stdout.splitlines():
        if not line or "Python" not in line:
            continue
        pid = pattern.findall(line)[0]
    if pid:
        logger.warn("The port %s is in used by process which pid=%s, we are trying to kill it." % (port, pid))
        [run_cmd(["kill", pid]) for _ in range(2)]


def run_server(data, host, port, queue):
    try:
        ret = connect_central_server(data, host, port)
    except:
        logger.error(traceback.format_exc())
        return
    if "success" not in ret.lower():
        logger.error(ret)
        return
    else:
        logger.info(ret)
    server = WSGIServer((host, port), WSGIRequestHandler)
    queue.put(server)
    server.set_app(qauto)
    logger.info("Start sub-server http://%s:%s" % (host, port))
    server.serve_forever()


def server_monitor(data, host, port, queue):
    status = False
    logger.info("Start watching sub-server status ...")
    while True:
        if status is False:
            server_thread = threading.Thread(target=run_server, args=(data, host, port, queue))
            server_thread.setDaemon(False)
            server_thread.start()
            status = True
        _host = get_localhost()
        if host != _host:
            logger.warn("Sub-server's host is changed to %s, restart sub-server." % _host)
            server = queue.get() or None
            if server is None:
                break
            server.shutdown()
            status = False
            host = _host
        delay_after_operation(10)


def http_server_start(data):
    """启动子服务器"""
    queue = Queue()
    host = get_localhost()
    port = data.port
    # 刚启动服务器时, 需要先检测端口占用情况, 如果被占用则尝试释放
    release_port(port)

    minotor_thread = threading.Thread(target=server_monitor, args=(data, host, port, queue))
    minotor_thread.setDaemon(False)
    minotor_thread.start()
