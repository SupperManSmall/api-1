# coding=utf-8
__author__ = 'xcma'
import urllib, urllib2, json, requests
import Run
import unittest, os, shutil, cookielib
from ReadConfig import readConfig
from LogMainClass import Log
from Utils import ABSpath
import json ,time, sys

# utf-8
reload(sys)
sys.setdefaultencoding('utf8')
log = Log('Methods')
Config_path_ym = ABSpath()+"/Src/Conf/Config.yml"
cookfile_path = ABSpath() + readConfig(Config_path_ym)['path']['global_dir']
cookfile_name = readConfig(Config_path_ym)['cookfile_name']

# 获取主域名
input_url = Run.url_target
url_category = "url_off"
if input_url in "www.xxtao.com":
    url_category = "url_off"
elif input_url in "www.wanpinghui.com":
    url_category = "url_on"
else:
    url_category = "url_off"
url_all = readConfig(Config_path_ym)[url_category]
if ',' not in url_all:
    main_domain = url_all
else:
    main_domain = url_all.split(',')[0]
log.warning('main_domain => %s' % main_domain)

class Api_urllib(unittest.TestCase):
    """
    api的所有方法
    """
    @classmethod
    def getInterface_requests_status(cls, parmeter={}, headers={}, path='/index.php', method='GET', data={}):
        """
        requests接口访问
        :param parmeter:
        :param headers:
        :param path:
        :param method:
        :return:
        """
        url = main_domain+path

        try:
            response = requests.request(method, url, headers=headers, params=parmeter, data=data)

            try:
                log.debug(response.text)
            except:
                log.debug(response.json())
            status_code = response.status_code

            log.debug('status:%s' % status_code)
            if Api_urllib.get_status_code(status_code):
                try:
                    return response.json(), status_code
                except:
                    return response.text, status_code
            else:
                return "Error", status_code

        except Exception as msg:
            log.error(msg)
            print (msg)
            raise


    @classmethod
    def getInterface_requests(cls, parmeter, headers={}, path='/index.php', method='GET', data={}):
        """
        requests接口访问
        :param parmeter:
        :param headers:
        :param path:
        :param method:
        :return:
        """
        url = main_domain+path

        try:
            response = requests.request(method, url, headers=headers, params=parmeter, data=data)

            try:
                log.debug(response.text)
            except:
                log.debug(response.json())
            status_code = response.status_code
            log.debug('status:%s' % status_code)
            if Api_urllib.get_status_code(status_code):
                try:
                    return response.json()
                except:
                    return response.text
            else:
                return status_code

        except Exception as msg:
            log.error(msg)
            print (msg)
            raise

    @classmethod
    def get_status_code(cls, status_code):
        """
        获取到当前返回状态码:若成功或者重定向,返回True,否则False
        :param status_code:
        :return:
        """

        code = {

            400,
            401,
            402,
            403,
            404,
            405,
            406,
            407,
            408,
            409,
            410,
            411,
            412,
            413,
            414,
            415,
            416,
            417,
            418,
            422,
            423,
            424,
            425,
            426,
            428,
            429,
            431,
            449,
            450,
            500,
            501,
            502,
            503,
            504,
            505,
            507,
            508,
            509,
            510,
            511
        }
        if status_code in code:
            return False
        return True

    @classmethod
    def getInterface(cls, parameter=None, headers={}, path='/index.php?'):
        """
        parameter = {"r": "demand/info", "demand_id": '2938'}格式
        :param parameter:
        :param headers:
        :param path:
        :return:
        """
        #获取请求url
        try:
            get_url = main_domain + path
            log.debug('get_url:' + get_url)
            log.debug(u'获取请求url')
            # 解析请求参数
            params = urllib.urlencode(parameter)
            log.debug(u'解析请求参数:' + params)
            send_url = get_url + params
            log.debug(u'拼装成功url:' + send_url)
            # 访问接口
            req = urllib2.Request(send_url, headers=headers)
            log.debug(u'访问接口')
            # 打印请求日志:
            # httpHandler = urllib2.HTTPHandler(debuglevel=1)
            # httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
            # opener = urllib2.build_opener(httpHandler, httpsHandler)
            # urllib2.install_opener(opener)
            # 读取返回值
            response = urllib2.urlopen(req).read()
            log.debug(response)
            # 解析json格式读取
            if response[response.find('<', 0):1] != '<':
                json_result = json.loads(response)
                log.debug(u'解析json格式读取')
                return json_result
            else:
                return response
        except Exception as msg:
            log.error(u'接口访问异常')
            log.exception(msg)
            print msg
            raise

    @classmethod
    def postInterface(cls, parameter=None, headers={}, data={}):
        """
        parameter = {"r": "demand/info", "demand_id": '2938'}格式
        :param parameter:
        :param headers:
        :param data:
        :return:
        """
        # 获取请求url
        try:
            get_url = main_domain+'/index.php?'
            log.debug('get_url:'+get_url)
            log.debug(u'获取请求url')
            #解析请求参数parameter、data
            params = urllib.urlencode(parameter)
            log.debug(u'解析请求参数:'+params)
            log.debug(u'拼装成功url:'+get_url+params)
            send_url = get_url + params
            send_data = urllib.urlencode(data)
            #访问接口
            req = urllib2.Request(send_url, data=send_data, headers=headers)
            log.debug(u'接口调用成功')
            #打印请求日志:
            # httpHandler = urllib2.HTTPHandler(debuglevel=1)
            # httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
            # opener = urllib2.build_opener(httpHandler, httpsHandler)
            # urllib2.install_opener(opener)
            #读取返回值
            response = urllib2.urlopen(req).read()
            log.debug(response)
            log.debug(u'返回值类型'+str(type(response)))
            #解析json格式读取
            res = str(response)
            if res[res.find('<', 0):1] != '<':
                json_result = json.loads(response)
                log.debug(u'解析json格式读取')
                return json_result
            else:
                return response
        except Exception as msg:
            log.error('访问接口异常')
            log.exception(msg)
            print (msg)
            raise

    @classmethod
    def upload_file(cls, file_name, file_path, parameter, parameter_name='pic', file_type='image/jpeg', headers={}, path='/index.php?'):
        params = urllib.urlencode(parameter)
        url = main_domain + path+params
        file_path_name = file_path+file_name
        files = {
            parameter_name: (file_name, open(file_path_name, 'rb'), file_type),
        }
        response = requests.post(url, files=files, headers=headers)
        log.debug(response.text)
        status_code = response.status_code
        if Api_urllib.get_status_code(status_code):
            try:
                return response.json(), status_code
            except:
                return response.text, status_code
        else:
            return 'Error', status_code

    @classmethod
    def getCookie(cls, parameter):
        u'获取cookie内容'
        try:
            params = urllib.urlencode(parameter)
            # response = Api_urllib.getInterface(parameter)
            response, status_code = Api_urllib.getInterface_requests_status(parameter)
            if response['succ'] != '0':
                url = main_domain+'/index.php?'+params
                # log.debug(u'生成的url:'+url)
                cookie = cookielib.CookieJar()
                handle = urllib2.HTTPCookieProcessor(cookie)
                opener = urllib2.build_opener(handle)
                opener.open(url)
                # log.debug(cookie)
                d = ""
                for item in cookie:
                    name = item.name
                    value = item.value
                    dic = name + "=" + value
                    d = dic+";"+d
                log.debug('cookie:' + str(d))
                dic1 = {"Cookie": d}
                return response, dic1
            else:
                return 'ERROR', status_code
        except Exception as msg:
            log.error('接口访问异常')
            print (msg)
            raise

    @classmethod
    def save_cookie_as_file(cls, cookie, who="100"):
        """
        将cookie保持在文件中,wph/xxtao分开保存
        :param cookie: 传入cookie
        :param who: 100-》工程商 1-》用户  保持文件路径不同
        :return:
        """
        if input_url in 'www.xxtao.com':
            if who =='100':
                cookieFile = cookfile_path+cookfile_name['supplier_xxtao']
            else:
                cookieFile = cookfile_path+cookfile_name['client_xxtao']
        else:
            if who =='100':
                cookieFile = cookfile_path+cookfile_name['supplier_wph']
            else:
                cookieFile = cookfile_path+cookfile_name['client_wph']
        try:
            fp = open(cookieFile, 'w')
            fp.write(str(cookie))
            log.debug(u'保持cookie成功')
        except Exception as msg:
            log.error(u'写文件失败')
            raise msg
        finally:
            fp.close()

    @classmethod
    def read_cookie_file(cls, who="100"):
        """
        读取cookie保持文件中的内容，重写内容
        :param who: who: 100-》工程商 1-》用户  保持文件路径不同
        :return:
        """
        if input_url in 'www.xxtao.com':
            if who == '100':
                cookieFile = cookfile_path+cookfile_name['supplier_xxtao']
            else:
                cookieFile = cookfile_path+cookfile_name['client_xxtao']
        else:
            if who == '100':
                cookieFile = cookfile_path+cookfile_name['supplier_wph']
            else:
                cookieFile = cookfile_path+cookfile_name['client_wph']
        try:
            fp = open(cookieFile, 'r+')
            cookie = fp.read()

            # 将字符串转换为字典 eval
            return eval(cookie)
        except Exception as msg:
            log.error(u'读文件失败')
            raise msg
        finally:
            fp.close()

    @classmethod
    def save_as_file(cls, comments, file_name='demand', write='a'):
        """
        追加文件内容
        :param comments:
        :return:
        """
        file_name = cookfile_path + file_name
        fp = open(file_name, write)
        try:
            fp.write(str(comments) + ',')
            log.debug('save as file ok')
        except Exception as msg:
            log.error('write error')
            raise msg
        finally:
            fp.close()

    @classmethod
    def read_from_file(cls, file_name='demand_id'):

        file_name_and_path = cookfile_path + file_name
        for file in os.listdir(cookfile_path):
            if file == file_name:
                fp = open(file_name_and_path, 'r+')
                try:
                    comment = fp.read()
                    # 将字符串转换为字典 eval
                    try:
                        return eval(comment)
                    except:
                        return comment
                except Exception as msg:
                    log.error(u'读文件失败')
                    raise msg
                finally:
                    fp.close()
        else:
            log.warning('read_file =>Fail')
    @classmethod
    def save_cookie(cls, parameter):
        """
        将需要的cookie保存在指定文件中
        :param parameter:
        :return:
        """
        params = urllib.urlencode(parameter)
        url = main_domain+'/index.php?'+params
        log.debug(u'访问的url:'+url)
        log.debug(u'保存txt存放位置:"./Conf/Cookies_saved.txt"')
        cookieFile = ABSpath()+"/Output/Cookies_saved.txt"
        cookieJar = cookielib.MozillaCookieJar(cookieFile)
        log.debug(u'创建MozillacookiJar实例')
        log.debug(u'输出cookieJar:'+str(cookieJar))
        cookieJar.save()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        # open a url and  urllib2 will auto handle cookies
        response = opener.open(url)
        log.debug(response)
        cookieJar.save()

    @classmethod
    def openUrl_with_cookie(cls, parameter):
        u'打开需要调用的接口带着cookie访问,并传参parameter'
        cookieFile = ABSpath() + "/Output/Cookies_saved.txt"
        params = urllib.urlencode(parameter)
        url = main_domain+'/index.php?'+params
        log.debug(u'访问的url:'+url)
        cookie = cookielib.MozillaCookieJar('Cookies.txt')
        cookie.load(cookieFile)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        opener.open(url)

    @classmethod
    def del_demand(cls, demand_id):
        parameter = {"r": "demand/del-test", "demand_id": demand_id}
        header = {'X-Test-App': "chaoren", 'X-Test-Key': "notecode"}
        response = Api_urllib.getInterface_requests(parameter, header)
        log.debug(u'del_demand => ok')
        return response

    @classmethod
    def del_demand_who(cls):
        """
        删除指定用户的搜索报装屏幕demand，当前默认是cookie中的客户
        :return:
        """
        cookie = Api_urllib.read_cookie_file('1')
        parameter = {"r": "demand/list"}
        response = Api_urllib.getInterface_requests(parameter, headers=cookie)
        for i in range(0, len(response['list'])):
            demand_id = response['list'][i]['demand_id']
            Api_urllib.del_demand(demand_id)

    @classmethod
    def todo_string(cls, string):
        """
        返回值response为字符串时调用此方法
        :param string:
        :return:
        """
        return string.replace('\n', '').replace(' ', '')[0:20]

class Os:

    @classmethod
    def get_now_time(cls):
        """
        获取当前时间，格式为：YY:MMM:DD HH:MM:SS
        :return:
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    @classmethod
    def del_file(cls, dir, filename):
        u'删除指定目录dir中的指定file'
        cls.dir = str(dir)
        for file in os.listdir(cls.dir):
            if file != filename:
                os.remove(cls.dir + file)
        log.debug(u'删除成功')

    @classmethod
    def del_file_specific(cls, dir, filename):
        '''

        删除与参数相同的文件
        '''
        cls.dir = str(dir)
        for file in os.listdir(cls.dir):

            if file == filename:
                os.remove(cls.dir + file)
            else:
                continue

    @classmethod
    def new_report_nopath(cls, reportpath):
        '''
        对test_report目录中文件进行排序，返回最新生成的html文件
        '''

        lists = os.listdir(reportpath)
        lists.sort(key=lambda fn: os.path.getmtime(reportpath + '/' + fn))

        if lists[-1] == ".DS_Store":
            file_new = os.path.join(lists[-2])
        else:
            file_new = os.path.join(lists[-1])
        return file_new

    @classmethod
    def new_report_path(cls, reportpath):
        '''
        对test_report目录中文件进行排序，返回最新生成的html文件
        '''

        lists = os.listdir(reportpath)
        lists.sort(key=lambda fn: os.path.getmtime(reportpath + '/' + fn))
        if lists[-1] == ".DS_Store":
            file_new = reportpath + os.path.join(lists[-2])
        else:
            file_new = reportpath + os.path.join(lists[-1])
        return file_new

    @classmethod
    def move_file(cls, oldpath, newpath):
        '''
        移动文件到目标路径
        '''
        try:

            shutil.move(oldpath, newpath)
        except BaseException as msg:
            print msg

    @classmethod
    def copy_file(cls, filepath, newpath):
        '''
        复制指定文件到目标目录
        '''
        try:

            shutil.copy(filepath, newpath)
        except BaseException as msg:
            print msg

