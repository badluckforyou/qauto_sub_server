import sys
import ujson as json
import hashlib
import threading

from importlib import import_module
from traceback import format_exc

from common.log import logger


BYTE_ERROR = "Sub-server gets nothing to start automated testing."
JSON_ERROR = "Data parse failed. \nError: %s"
DATA_ERROR = "Sub-server gets wrong data to start automated testing. \nError: %s"
USER_ERROR = "Username or password is wrong. \nError: %s"
UNEXCEPT_ERROR = "An unexpected error occurred.\nError: %s"
SUCCESS = "Automated testing starts success."



class CommandError(Exception):
    pass


def _hash_encrypted(entry):
    """md5加密"""
    _hash = hashlib.md5()
    _hash.update(entry.encode("utf-8"))
    return _hash.hexdigest()


def load_command_module(module, method):
    """方法引用"""
    try:
        module = import_module("platforms.%s" % module)
    except ImportError: raise CommandError
    
    if hasattr(module, method):
        return getattr(module, method)
    else: raise CommandError


def http_monitor(environ):
    try:
        request_queue_size = int(environ["CONTENT_LENGTH"])
    except:
        request_queue_size = 0

    file_encoding = sys.getfilesystemencoding()

    result = list()
    if environ["REQUEST_METHOD"] == "GET":
        data = "<h3>Success<h3>"

    elif environ["REQUEST_METHOD"] == "POST":
        wsgi_data = environ["wsgi.input"].read(request_queue_size)

        if wsgi_data == b"":
            data = BYTE_ERROR
        else:
            try:
                post_data = json.loads(wsgi_data.decode(file_encoding))
                try:
                    username = post_data["username"]
                    try:
                        id = post_data["id"]
                        platform = post_data["platform"]
                        testcase = post_data["testcase"]
                        project  = post_data["project"]
                        package  = post_data["package"]
                        function = load_command_module(platform, project.lower())
                        thread = threading.Thread(target=function, args=(id, username, project, package, testcase))
                        thread.setDaemon(True)
                        thread.start()
                        data = SUCCESS
                    except:
                        data = UNEXCEPT_ERROR % format_exc()
                except:
                    data = DATA_ERROR % format_exc()
            except:
                data = JSON_ERROR % format_exc()
        logger.info(data)
    result.append(data.encode(file_encoding))
    return result

    