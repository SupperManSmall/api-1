# coding:utf-8
__author__ = 'xcma'

from Src.Function.ApiMethod import *
from Src.Function.LogMainClass import *
from Src.Function.MySql import MySQL
import Run
casename = '获取b44返回值字典'
log = Log(casename)
main_domain = Run.url_target

class ConfDict(Api_urllib):
    '''获取b44返回值字典'''
    def setUp(self):
        log.debug('setUp')
        self.comment = casename
        self.casename = "test_A_confDict"
        self.interfacename = 'b45'
        self.result = 'Fail'
        self.response = "Null"
        self.status = '0'
    if main_domain in 'www.xxtao.com':
        def test_A_DemandB45(self):
            log.debug(self.casename + ':start')
            response = ''
            status_code = ''
            try:
                parameter = {"r": "conf/dict"}
                response, status_code = Api_urllib.getInterface_requests_status(parameter)
                self.assertTrue(response. has_key('succ'))

                if response['succ'] == '1':
                    self.assertTrue(response['demand']. has_key('loc'))
                    self.result = 'Pass'
                else:
                    self.assertTrue(response. has_key('msg'))

            except Exception as msg:
                log.error("接口访问异常")
                log.error(msg)
                raise msg
            log.debug(casename + ':done')

    def tearDown(self):
        log.debug('tearDown')