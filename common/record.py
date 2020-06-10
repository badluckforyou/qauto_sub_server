import sys
import time
import traceback

from functools import wraps

from common.helper import time_covered_bracket, delay_after_operation, FormatTime, Logger
from common.log import logger



class Record:

    @staticmethod
    def monitor(func):
        """
        AppiumRefactor及SeleniumRefactor所需要用到的修饰器
        用来记录各种操作的执行时间及其它某些处理
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            begin_time = time.time()
            # 在外部传进delay参数来控制sleep
            # 以避免在AppiumTranslation中大量增加sleep代码
            # 该参数在获取到对应值后要pop删除掉以避免func因参数数量错误而报错
            if "delay" in kwargs:
                delay = kwargs["delay"]
                # 将delay删除以免报错
                kwargs.pop("delay")
            else:
                delay = 0
            # 执行func并对报错进行打印
            try:
                ret = func(self, *args, **kwargs)
            except Exception:
                Logger.error(traceback.format_exc())
                # 打印报错
                logger.error(traceback.format_exc())
            else:
                # 延时, 仅在成功时执行, 失败了便无需等待
                if delay:
                    delay_after_operation(delay)
                return ret
            finally:
                msg = "%s %s%s finished in %s. Args: " % (self.__class__.__name__, 
                                                            func.__name__, 
                                                            " " * (5 - len(func.__name__)),
                                                            FormatTime.format(time.time() - begin_time))
                for arg in args:
                    if arg == args[-1]:
                        if isinstance(arg, list):
                            arg = ", ".join(arg)
                            msg += "[{}]".format(arg)
                        else:
                            msg += arg
                    else:
                        if isinstance(arg, list):
                            arg = ", ".join(arg)
                            msg += "[{}], ".format(arg)
                        else:
                            msg += "{}, ".format(arg)
                Logger.info(msg)
                logger.info(msg)
        return wrapper

    @staticmethod
    def finish(f):
        """完成时打印执行时长"""
        @wraps(f)
        def wrapper(*args):
            start_time = time.time()
            f(*args)
            cost_time = time.time() - start_time
            logger.info(
                "================== Finished in %s. "
                "==================" % FormatTime.format(cost_time))
        return wrapper


