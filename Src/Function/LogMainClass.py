# coding=utf-8
__author__ = 'xcma'

import logging
import logging.handlers
from ReadConfig import readConfig
import time, os,sys
import platform
import Run
from Src.Function.Utils import *

rq = time.strftime('%Y%m%d', time.localtime(time.time()))

class Log(logging.Logger):
    """日志类
    1.控制日志的输出格式
    2.控制日志的保存方式
    3.控制日志的保存路径
    4.控制日志是否在ide中打印
    """
    def __init__(self, name=None):
        super(Log, self).__init__(self)
        #建立Log目录
        new_dirname = "Log"
        new_path = os.path.join(ABSpath()+"/Output", new_dirname)
        Config_path = ABSpath()+"/Src/Conf/Config.yml"
        level = Run.log
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        # 日志文件名
        if name is None:
            name = 'my.log'

        # 定义log存储路径
        if platform.system() == 'Windows':
            self.path = ABSpath() + readConfig(Config_path)['log']['path_win']
        elif platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.path = ABSpath() + readConfig(Config_path)['log']['path_mac']

        self.filename = self.path+rq + '.log'

        self.name = name
        self.logger = logging.getLogger(self.name)
        # 创建一个handler，用于写入日志文件 (每天生成1个，保留10天的日志)
        fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 10)

        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d] - %(message)s')
        fh.setFormatter(formatter)
        self.addHandler(fh)

        # 再创建一个handler，用于输出到控制台
        self.logger = logging.getLogger(self.name)
        self.logger = logging.getLogger(self.name)
        ch = logging.StreamHandler()
        logger = logging.getLogger(self.name)
        ch = logging.StreamHandler()
        if level in 'debug':
            ch.setLevel(logging.DEBUG)
        elif level in 'info':
            ch.setLevel(logging.INFO)
        elif level in 'error':
            ch.setLevel(logging.ERROR)
        elif level in 'notset':
            ch.setLevel(logging.NOTSET)
        else:
            ch.setLevel(logging.WARNING)
        # 定义handler的输出格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d] - %(message)s')
        ch.setFormatter(formatter)
        # 给logger添加handler
        self.addHandler(ch)



"""记录用例执行步骤,等提供跟踪用例执行过程的相关信息
        :param msg:
        :return:
        self.logger.info(msg)

        针对异常需要警告的地方设置log记录
        :param msg:
        :return:
        self.logger.warning(msg)

        严重错误,需要人工跟踪的,严重影响系统的问题
        :param msg:
        :return:
        self.logger.error(msg)


        需要跟踪某些方法的返回值是否符合预期,主要针对跟踪方法轨迹
        :param msg:
        :return:
        self.logger.debug(msg)

        一般不启用该警告,暂时定为error为最高等级
        :param msg:
        :return:
        self.logger.critical(msg)

        self.logger.removeHandler(self.fh)

        接收全部异常处理生成的msg,并加入日志中,所有异常抛出全部用该方法接收,一般跟在except BaseException as msg:后面
        except BaseException as msg:
            logger.exception(msg)

        self.logger.exception(msg)"""


class customError(Exception):
    u'''
    自定义异常类,用在主动输出异常时使用,用 raise关键字配合使用,例:
            if True:
                pass
            else:
                raise customError(msg)
    '''
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        if self.msg:
            return self.msg
        else:
            return u"某个不符合条件的语法出问题了"

