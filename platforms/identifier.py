
import sys
import traceback

from core.ui.web import WebSelenium
from core.ui.ios import iOSAppium
from core.ui.android import AndroidAppium
from common.log import logger
from common.exceptions import SessionError



__author__ = "Jackey"



class AndroidSession:
    """appium iOS 连接模块"""

    session = None
    DRIVER = None

    @classmethod
    def connect(cls):
        if cls.session is None:
            logger.error("Couldn't connect android because the session is None.")
            raise SessionError
        logger.info("Appium android starts connecting.")
        cls.DRIVER = AndroidAppium(cls.session)
        logger.info("Appium android connects finished.")


class iOSSession:
    """appium iOS 连接模块"""

    session = None
    DRIVER = None

    @classmethod
    def connect(cls):
        if cls.session is None:
            logger.error("Couldn't connect iOS because the session is None.")
            raise SessionError
        logger.info("Appium iOS starts connecting.")
        try:
            cls.DRIVER = iOSAppium(cls.session)
        except:
            logger.error(traceback.format_exc())
        logger.info("Appium iOS connects finished.")


class ExecutablePath:
    """selenium web 连接模块"""
    
    executable_path = None
    DRIVER = None

    @classmethod
    def connect(cls):
        if cls.executable_path is None:
            logger.error("Couldn't open web because the executable_path is None.")
            raise SessionError
        logger.info("Selenium web starts connecting.")
        cls.DRIVER = WebSelenium(cls.executable_path)
        logger.info("Selenium web connects finished.")