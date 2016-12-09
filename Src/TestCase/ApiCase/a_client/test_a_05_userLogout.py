# coding:utf-8
__author__ = 'xcma'

from Src.Function.ApiMethod import *
from Src.Function.LogMainClass import *
from Src.Function.MySql import MySQL
casename = u'注销登录'
log = Log(casename)

class UserLogout(Api_urllib):
    u'''注销登录'''

    def setUp(self):
        log.debug('setUp')

    def test_A_UserLogout(self):
        u'1.注销登录_100'
        self.casename = 'user_type=100'
        casename = self.casename
        log.debug(casename + ':start')
        try:
            cookie = Api_urllib.read_cookie_file('100')
            parameter = {"r": "user/logout"}
            self.response, self.status_code = Api_urllib.getInterface_requests_status(parameter, headers=cookie)
            self.assertTrue(self.response. has_key('succ'))
            if self.response['succ'] != '1':
                self.assertTrue(self.response.has_key('msg'))
        except Exception as msg:
            log.error("接口访问异常")
            log.error(msg)
            print (msg)
            raise

        log.debug(casename + ':done')

    def test_B_UserLogout(self):
        u'1.注销登录_1'
        self.casename = 'user_type=1'
        casename = self.casename
        log.debug(casename + ':start')
        try:
            cookie = Api_urllib.read_cookie_file('1')
            parameter = {"r": "user/logout"}
            self.response, self.status_code = Api_urllib.getInterface_requests_status(parameter, headers=cookie)
            self.assertTrue(self.response. has_key('succ'))
            if self.response['succ'] != '1':
                self.assertTrue(self.response.has_key('msg'))
            self.result = 'Pass'
        except Exception as msg:
            log.error("接口访问异常")
            log.error(msg)
            print (msg)
            raise


        log.debug(casename + ':done')

    def tearDown(self):
        log.debug('tearDown')