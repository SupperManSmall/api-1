# coding:utf-8
__author__ = 'xcma'

from Src.Function.ApiMethod import *
from Src.Function.LogMainClass import *
from Src.Function.MySql import MySQL

casename = u'获取城市列表'
log = Log(casename)

class CityList(Api_urllib):
    u'''获取城市列表'''

    def setUp(self):
        log.debug('setUp')
        self.comment = casename
        self.casename = 'test_A_CityList'
        self.interfacename = 'a08'
        self.status_code = '0'
        self.result = 'Fail'
        self.response = "OK"

    def test_A_CityList(self):
        u'1.获取城市列表'
        log.debug(casename + ':start')
        try:
            parameter = {"r": "city/list"}
            self.response, self.status_code = Api_urllib.getInterface_requests_status(parameter)

            self.assertEqual(self.response['succ'], '1')
            self.assertIsNotNone(self.response['list']['A'])
            if self.response['succ'] == '1':
                self.result = 'Pass'
        except Exception as msg:
            log.error("接口访问异常")
            log.error(msg)
            print (msg)
            raise

        log.debug(casename + ':done')

    def tearDown(self):
        log.debug('tearDown')
