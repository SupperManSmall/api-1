# coding:utf-8
__author__ = 'xcma'

from Src.Function.ApiMethod import *
from Src.Function.LogMainClass import *
from Src.Function.MySql import MySQL
casename = u'检查手机是否已经登录过'
log = Log(casename)


class UserDengji(Api_urllib):
    """检查手机是否已经登录过"""

    def setUp(self):
        log.debug('setUp')
        self.comment = casename
        self.casename = ''
        self.interfacename = 'a07'
        self.status = '0'
        self.result = 'Fail'
        self.response = "OK"

    def test_A_userCheckphone_1(self):
        "1.a07-usertype=1"
        self.casename = 'user_type=1'
        casename = self.casename
        log.debug(casename + u':开始执行')
        try:
            parameter = {"r": "user/checkphone", "phone": "10000000000", "user_type": "1"}
            self.response, self.status_code = Api_urllib.getInterface_requests_status(parameter)
            self.assertTrue(self.response. has_key('succ'))
            self.result = 'Pass'
        except Exception as msg:
            log.error("Excepthon Logged")
            log.error(msg)
            print (msg)
            raise

        log.debug(casename + u':执行完毕')

    def test_A_userCheckphone_100(self):
        "2.a07-usertype=100"
        self.casename = 'user_type=100'
        casename = self.casename
        log.debug(casename + u':开始执行')
        try:
            parameter = {"r": "user/checkphone","phone": "10000000009", "user_type": "100"}
            self.response, self.status_code = Api_urllib.getInterface_requests_status(parameter)
            self.assertTrue(self.response. has_key('succ'))
            self.result = 'Pass'
        except Exception as msg:
            log.error("Excepthon Logged")
            log.error(msg)
            print (msg)
            raise

        log.debug(casename + u':执行完毕')

    def tearDown(self):
            log.debug('tearDown')