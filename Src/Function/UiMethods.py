# coding=utf-8
__author__ = 'xcma'
import unittest, datetime, time, os, shutil, platform
import random, requests, json, sys, Run
from selenium import webdriver
from ReadConfig import readConfig
from LogMainClass import Log
from selenium.webdriver import ActionChains
from Utils import ABSpath
log = Log(name='Methods')
log.debug('Selenium version:%s' % webdriver.__version__)
Config_path = ABSpath() + "/Src/Conf/Config.yml"
class Operation(unittest.TestCase):

    u'''
    浏览器相关操作
    '''
    @classmethod
    def open_browser(cls, chrome_options=None):
        choosebrower = Run.brower
        if choosebrower in 'chrome':
            log.debug(u'调用Chrome')
            cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        elif choosebrower in 'firfox' :
            log.debug(u'调用Firefox')
            cls.driver = webdriver.Firefox()
        elif choosebrower in 'phantomjs':
            cls.driver = webdriver.PhantomJS('phantomjs')
            log.debug(u'调用phantomjs')
        else:
            cls.driver = webdriver.Chrome()
            log.debug(u'调用Firefox')
        # if platform.system() == 'Linux': # CentOS上安装chrome不成功，不得不用Firefox
        #     log.debug(u'调用Firefox')
        #     cls.driver = webdriver.Firefox()
        # else:
        #     log.debug(u'调用Chrome')
        #     cls.driver = webdriver.Chrome(chrome_options=chrome_options)

        # 隐式等待
        cls.driver.implicitly_wait(10)
        cls.driver.set_window_size(1480, 978)
        # cls.driver.maximize_window()

    @classmethod
    def chrome_options(cls):
        mobile_emulation = {
            "deviceMetrics": {"width":375, "height": 667, "pixelRatio": 2.0},
            #"userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
            "userAgent":"Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
            }
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        return chrome_options

    @classmethod
    def url_target_Choose(cls, modules_path="/"):
        """
        默认选中:pc_xxtao
        可选值:
        1.m     = {m}
        2.pc    = {pc}
        3.api   = {api,a}
        :param modules_path:
        :return:
        """
        driver = cls.driver
        input_url = Run.url_target

        # 定义全部url列表
        url = readConfig(Config_path)
        if input_url in "www.xxtao.com":
            cls.url_category = "url_off"
        elif input_url in "www.wanpinghui.com":
            cls.url_category = "url_on"
        else:
            cls.url_category = "url_off"
        url_all = []
        read_url = url[cls.url_category]
        log.debug("read_url:%s" % read_url)
        url_by = read_url.split(',')
        for u in url_by:
            url_all.append(u)
        log.debug("url_all：%s" % url_all)
        if ',' not in modules_path:
            driver.get(url_all[2] + modules_path)
        url_by = modules_path.split(',')[0]
        modules_path_value = modules_path.split(',')[1]
        # m端
        if url_by == 'm' or url_by == 'M':
            driver.get(url_all[1] + modules_path_value)
            log.warning('main_domain=>'+url_all[1]+modules_path_value)
            return url_all[1]+modules_path_value
        # pc端
        if url_by == 'p' or url_by == 'P':
            driver.get(url_all[2] + modules_path_value)
            log.warning('main_domain=>' + url_all[2]+modules_path_value)
            return url_all[2]+modules_path_value
        # api 接口
        if url_by in 'api' or url_by in 'API':
            driver.get(url_all[0] + modules_path_value)
            log.warning('main_domain=>' + url_all[0]+modules_path_value)
            return url_all[0]+modules_path_value

    @classmethod
    def get_status_code(cls, modules_path=''):
        u'''获取到当前页面链接,校验返回状态码:若成功或者重定向,返回True,否则False'''
        now_url = cls.driver.current_url
        modules_path = str(modules_path)
        log.debug('now_url:%s' % now_url)
        status_code = requests.get(now_url+modules_path).status_code
        log.debug(status_code)
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
            return False, status_code
        return True, status_code

    @classmethod
    def Processing_page_state(cls, msg='页面打开失败'):
        u'''
        处理页面返回状态码,若状态码=True,则通过,否则抛出异常
        :param msg:
        :return:
        '''
        try:
            result, status_code = Operation.get_status_code()
            if result:
                return status_code
            else:
                log.error(msg)
                raise msg
        except Exception as msg:
            log.error(msg)
            raise msg
    @classmethod
    def close_browser(cls):
        cls.driver.quit()

    @classmethod
    def Truescreenshot(cls, casename):
        """截图放到相应路径中"""
        cname = casename +datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]

        #截图创建路径
        TrueScreenshotPath = Os.ABSpath()+readConfig(Config_path)['path']['TrueScreenshot']
        log.debug(u'读取截图路径：'+str(TrueScreenshotPath))
        Os.mkdir(path=Os.ABSpath()+"/Output/Screenshot", name='Pass')
        cls.driver.get_screenshot_as_file(TrueScreenshotPath+"%s.png" % cname)
        log.debug(u'True截图成功')

    @classmethod
    def Falsecreenshot(cls, casename):
        """截图放到相应路径中"""
        cname = casename + datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
        # 截图创建路径
        FalseScreenshotPath = Os.ABSpath()+readConfig(Config_path)['path']['FalseScreenshot']
        log.debug(u'读取截图路径：' + str(FalseScreenshotPath))
        Os.mkdir(path=Os.ABSpath()+"/Output/Screenshot", name='Fail')
        cls.driver.get_screenshot_as_file(FalseScreenshotPath+"%s.png" % cname)
        log.debug(u'False截图成功')
    @classmethod
    def wait(cls, waittime=3):
        time.sleep(waittime)

    @classmethod
    def refreshBrowser(cls):
        """
        刷新浏览器
        :return:
        """
        cls.driver.refresh()

    @classmethod
    def current_handle(cls):
        '''
        获取当前窗口handle，记录当前窗口标签
        '''
        driver = cls.driver
        currentHandle = driver.current_window_handle

        return currentHandle

    @classmethod
    def all_handle(cls):
        '''
        获取全部窗口handle,记录全部窗口标签
        '''
        driver = cls.driver
        allHandle = driver.window_handles
        return allHandle

    @classmethod
    def switch_window(cls, currentHandle, allHandle):
        '''
        切换窗口，选中非当前窗口，即切换回原来窗口
        '''
        driver = cls.driver
        for table in allHandle:
            if table != currentHandle:

                log.debug(u'切换回原窗口Handle:'+table)
                return driver.switch_to_window(table)

    @classmethod
    def switch_to_iframe(cls, iframePath=None,idname='TrackFrame'):
        '''
        找到隐藏页面,并校验隐藏页面是否存在
        :return:
        '''
        #执行js,将隐藏页面变为显示状态
        try:
            driver = cls.driver
            Operation.rolling_to(y=4000)
            js = '''document.getElementById('Track').className = "";'''
            driver.execute_script(js)
            Operation.wait(1)
            Operation.rolling_to('4000')
            Operation.wait(1)
            iframe = Operation.getElement('i,'+idname)
            driver.switch_to_frame(iframe)
            Operation.wait(1)
            finded_iframe = Operation.getElement(".//*[@id='c']").text
            log.debug(finded_iframe)
            if cmp(iframePath, finded_iframe) == 0:
                log.debug(u'iframe校验成功')
            else:
                log.error(u'iframe校验失败')
                raise Exception
        except Exception as msg:
            log.error(u'查找隐藏页面失败')
            raise msg

    @classmethod
    def switchDefaultFrame(cls):
        """
        Returns the current form machine form at the next higher level.
        Corresponding relationship with switch_to_frame () method.

        Usage:
        driver.switch_to_frame_out()
        """
        cls.driver.switch_to.default_content()

    @classmethod
    def rolling_by(cls,target_element):
        '''
        滚动浏览器页面，查找目标元素
        '''
        driver = cls.driver
        while True:
            Operation.wait(1)
            if target_element:
                print '找到了'
                break
            else:
                driver.execute_script("window.scrollBy(0,100)")

    @classmethod
    def checkOver_bask_scr(cls, selector=None):
        """
        前往新页面,并检查新页面中元素-》确认到达新页面,然后关闭新页面,然后将焦点切换回原始页面.
        :param selector:
        :return:
        """
        driver = cls.driver
        try:
            now = Operation.current_handle()
            log.debug(now)
            all = Operation.all_handle()
            log.debug(all)
            Operation.switch_window(now, all)
            log.debug(u'切换到 新文章页 - 1')
            Operation.getElement(selector)
            log.debug(u'校验新打开页面正确性 - 通过')
            driver.close()
            log.debug(u'关闭当前屏幕 - 1')
            # 回到原始页
            Operation.wait(3)
            driver.switch_to_window(now)
            log.debug(u'切换选中屏幕到原始页 - 0')
        except Exception as msg:
            log.error('Exception Logged')
            print msg
            raise

    @classmethod
    def rolling_to(cls, y=0):
        '''
        滚动浏览器页面到指定位置,x是横向,y是纵向
        '''
        cls.y = str(y)
        driver = cls.driver
        target = "window.scrollTo(0" + "," + cls.y + ")"
        driver.execute_script(target)

    @classmethod
    def getElement(cls, selector):
        """
        to locate element by selector
        :arg
        selector should be passed by an example with "i,xxx"
        "x,//*[@id='langs']/button"
        :returns
        DOM element
        """
        driver = cls.driver
        try:
            if ',' not in selector:
                return driver.find_element_by_xpath(selector)
            selector_by = selector.split(',')[0]
            selector_value = selector.split(',')[1]
            if selector_by == "i" or selector_by == 'id':
                element = driver.find_element_by_id(selector_value)
            elif selector_by == "n" or selector_by == 'name':
                element = driver.find_element_by_name(selector_value)
            elif selector_by == "c" or selector_by == 'class_name':
                element = driver.find_element_by_class_name(selector_value)
            elif selector_by == "l" or selector_by == 'link_text':
                element = driver.find_element_by_link_text(selector_value)
            elif selector_by == "p" or selector_by == 'partial_link_text':
                element = driver.find_element_by_partial_link_text(selector_value)
            elif selector_by == "t" or selector_by == 'tag_name':
                element = driver.find_element_by_tag_name(selector_value)
            elif selector_by == "x" or selector_by == 'xpath':
                element = driver.find_element_by_xpath(selector_value)
            elif selector_by == "css" or selector_by == 'css_selector':
                element = driver.find_element_by_css_selector(selector_value)
            else:
                raise NameError("Please enter a valid type of targeting elements.")

            return element
        except Exception as msg:
            log.error('元素未找到')
            log.error(msg)
            raise msg

    @classmethod
    def is_displayed(cls, selector):
        """
        判断当前元素是否存在
        :param selector:
        :return:
        """
        element = Operation.getElement(selector)
        return element.is_displayed()

    @classmethod
    def get_text(cls, selector):
        """
        获取元素的text文本
        :param selector:
        :return:
        """
        element = Operation.getElement(selector)
        return unicode(element.text)

    @classmethod
    def get_text_attribute(cls, selector, attribute):
        """
        获取input框中默认文案
        :param selector:
                attribute:'value'
        :return:
        """
        element = Operation.getElement(selector)
        return element.getAttribute(attribute)

    @classmethod
    def get_url(cls):
        """
        Get the URL address of the current page.

        Usage:
        driver.get_url()
        """
        return cls.driver.current_url

    @classmethod
    def send_keys(cls, selector, text):
        """
        输入text
        :param selector:
        :param text:
        :return:
        """
        el = Operation.getElement(selector)
        el.clear()
        el.send_keys(text)

    @classmethod
    def element_click(cls, selector):
        """
        点击元素
        :param selector:
        :return:
        """
        element = Operation.getElement(selector)
        element.click()

    @classmethod
    def execute_Js(cls, script):
        """
        Execute JavaScript scripts.

        Usage:
        driver.js("window.scrollTo(200,1000);")
        """
        return cls.driver.execute_script(script)

    @classmethod
    def acceptAlert(cls):
        '''
            Accept warning box.
            同意alert弹窗
            Usage:
            driver.accept_alert()
            '''
        cls.driver.switch_to.alert.accept()

    @classmethod
    def dismissAlert(cls):
        '''
        Dismisses the alert available.
        拒绝alert弹窗
        Usage:
        driver.dismissAlert()
        '''
        cls.driver.switch_to.alert.dismiss()

    @classmethod
    def get_title(cls):
        """
        获取当前页面的title
        :return:
        """
        driver = cls.driver
        return driver.title

    @classmethod
    def GenerateDemand(cls):
        """
        10s报装需求,生成随机号码的新需求
        :return:
        """
        try:
            Operation.getElement(".//*[@id='IndexBookin']/div[2]/input[1]").click()
            log.debug(u'操作昵称输入框')
            Operation.getElement(".//*[@id='IndexBookin']/div[2]/input[1]").clear()
            Operation.getElement(".//*[@id='IndexBookin']/div[2]/input[1]").send_keys(u'自动化测试生成用户')
            Operation.getElement(".//*[@id='IndexBookin']/div[2]/input[2]").click()
            log.debug(u'操作手机号输入框')
            Operation.getElement(".//*[@id='IndexBookin']/div[2]/input[2]").clear()
            phone = UserLogin.enable_phone()
            log.debug(u'生成的手机号为:' + phone)
            Operation.getElement(".//*[@id='IndexBookin']/div[2]/input[2]").send_keys(phone)
            Operation.wait(1)
            Operation.getElement(".//*[@id='bd_10ssignup_submit']").click()
        except Exception as msg:
            log.error("Exception Logged")
            print msg
            raise

    @classmethod
    def implicitlyWait(cls, secs):
        """
        Implicitly wait. All elements on the page.
        隐式等待
        Usage:
        driver.implicitly_wait(10)
        """
        cls.driver.implicitly_wait(secs)

class Mouse(Operation):
    """定义鼠标的全部行为"""
    @classmethod
    def hovering(cls, element):
        """鼠标悬停"""
        # 定位到要悬停的元素
        try:
            driver = cls.driver
            above = Operation.getElement(element)
            # 对定位到的元素执行悬停操作
            ActionChains(driver).move_to_element(above).perform()
        except Exception as msg:
            log.error("Exception Logged")
            print msg
            raise

    @classmethod
    def right_click(cls, element):
        """鼠标右键点击"""
        try:
            driver = cls.driver
            # ****定位到要右击的元素**
            right_click = Operation.getElement(element)
            # ****对定位到的元素执行鼠标右键操作
            ActionChains(driver).context_click(right_click).perform()
        except Exception as msg:
            log.error("Exception Logged")
            print msg
            raise

    @classmethod
    def double_click(cls, element):
        """鼠标右键点击"""
        try:
            driver = cls.driver
            # 定位到要悬停的元素
            double_click = Operation.getElement(element)
            # 对定位到的元素执行双击操作
            ActionChains(driver).double_click(double_click).perform()
        except Exception as msg:
            log.error("Exception Logged")
            print msg
            raise

    @classmethod
    def drag_and_drop(cls, source, target):
        """鼠标拖动元素,从sourse到target"""
        try:
            driver = cls.driver
            # 定位元素的源位置
            element = Operation.getElement(source)
            # 定位元素要移动到的目标位置
            target = Operation.getElement(target)
            # 执行元素的拖放操作
            ActionChains(driver).drag_and_drop(element, target).perform()
            log.debug(u'移动鼠标到目标点')
        except Exception as msg:
            log.error("Exception Logged")
            print msg
            raise

class UserLogin(Operation):
    @classmethod
    def user_login(cls, phone):
        u'''新用户登录
        new_user = {'13111111111':'暂时不用','13111111112','13111111113','13111111114':'',
        '13111111115','13111111116','13111111117','13111111118','13111111119'}
        通用手机号集合,passcode:1234 --任意
        13111111112:无报装屏幕
        13111111113:有一个建设中屏幕
        13111111114:有建设完成的屏幕
        13111111116:工程商用户
        '''
        driver = cls.driver
        try:
            Operation.wait(2)
            driver.find_element_by_xpath(".//*[@id='CLoginForm']/form/div[1]/input").click()
            driver.find_element_by_xpath(".//*[@id='CLoginForm']/form/div[1]/input").clear()
            #phone = UserLogin.enable_phone()
            # phone = '13111111112'
            driver.find_element_by_xpath(".//*[@id='CLoginForm']/form/div[1]/input").send_keys(phone)
            log.debug(u'输入手机号')
            Operation.wait(1)
            driver.find_element_by_xpath(".//*[@id='CLoginForm']/form/div[2]/input").click()
            driver.find_element_by_xpath(".//*[@id='CLoginForm']/form/div[2]/input").clear()
            # passcode = UserLogin.get_passcode(phone)
            passcode = '1234'
            Operation.wait(0.5)
            log.debug(u'获取验证码')
            driver.find_element_by_xpath(".//*[@id='CLoginForm']/form/div[2]/input").send_keys(passcode)
            log.debug(u'输入验证码')
            driver.find_element_by_xpath(".//*[@id='CLoginForm']/form/button").click()
            log.debug(u"登录成功")
            Operation.wait(1)
        except Exception as msg:
            log.error("Exception Logged")
            raise msg

    @classmethod
    def log_out(cls):
        u'操作界面退出登录'
        driver = cls.driver
        try:
            # 退出登录
            driver.find_element_by_xpath(".//*[@id='Header']/div/div[3]/div[1]").click()
            log.debug(u'点击头像菜单')
            Operation.wait(3)
            driver.find_element_by_xpath(".//*[@id='Header']/div/div[3]/div[4]/div/a[2]").click()
            log.debug(u'退出登录')
        except Exception as msg:
            log.error("Exception Logged")
            print msg
            raise

    @classmethod
    def log_out_interface(cls, r="user/logout"):
        u'注销登录状态'
        url = readConfig(Config_path)['url_off'][0]
        log.debug(url)
        parameter = {"r": r}
        requests.get(url, params=parameter)
        log.debug(u'注销成功')

    @classmethod
    def get_passcode(cls, phone):
        u'获取验证码'
        url = readConfig(Config_path)['url_off'][0]
        parameter = {"r": "user/code", "phone": phone}
        r = requests.get(url, params=parameter)
        q = r.json()
        p = json.dumps(q, sort_keys=True)
        log.debug(u'获取验证码')
        return p[-3]

    @classmethod
    def generate_phone(cls):
        '''
        生成随机手机号
        '''
        phone = random.choice(['139', '188', '185', '136', '158', '151'])+"".join(random.choice("0123456789")
        for i in range(8))
        return phone

    # 验证接口返回值是否为1
    @classmethod
    def inter_validation(cls, r=None, phone=None, url=None):
        u'a07接口,返回值为1,则代表该手机号为老用户;此时重新生成手机号,直到接口返回值为:0'
        parameter = {"r": r, "phone": phone, "user_type": "1"}
        r = requests.get(url, params=parameter)
        q = r.json()
        p = json.dumps(q, sort_keys=True)
        if p[-3] == '1':
            return False
        else:
            return True

    # 创建首次访问网站手机号
    @classmethod
    def enable_phone(cls):
        url1 = cls.url_category
        while True:
            phone = UserLogin.generate_phone()
            url_all = readConfig(Config_path)[url1]
            url = url_all.split(',')[0]
            log.debug("url:%s" % url)
            if UserLogin.inter_validation(r='user/checkphone', phone=phone, url=url):
                return phone

class Os:
    """系统相关操作"""
    @classmethod
    def ABSpath(cls):
        """获取当前的绝对路径"""
        ABSPATH = os.path.abspath(sys.argv[0])
        ABSPATH = os.path.dirname(ABSPATH)
        return ABSPATH

    @classmethod
    def remove_file(cls,dir):
        u'删除路径中所有文件'
        cls.dir = str(dir)
        if os.path.isdir(cls.dir):
            for file in os.listdir(cls.dir):
                os.remove(cls.dir+file)
        else:
            log.error(u'删除失败')
            raise

    @classmethod
    def del_file(cls, dir, filename):
        """
        删除指定目录dir中与filename不同的文件
        :param dir:
        :param filename:
        :return:
        """
        cls.dir = str(dir)
        try:
            if os.listdir(dir):
                for file in os.listdir(cls.dir):
                    if file != filename:
                        os.remove(cls.dir + file)
                log.debug('del_file => ok')
        except Exception as msg:
            log.error('del_file => error')
            raise msg

    @classmethod
    def del_file_specific(cls, dir, filename):
        """
        删除与参数相同的文件
        :param dir:
        :param filename:
        :return:
        """
        cls.dir = str(dir)
        try:
            if os.listdir(cls.dir):
                for file in os.listdir(cls.dir):
                    if file == filename:
                        os.remove(cls.dir+file)
                log.debug('del_file => ok')
        except Exception as msg:
            log.error('del_file => error')
            raise msg

    @classmethod
    def del_file_the_earliest(cls, dir):
        """
        当删除指定目录dir中文件总数>50,删除最早的一个文件
        :param dir:
        :param filename:
        :return:
        """
        cls.dir = str(dir)
        if not os.listdir(dir):
            log.debug(u'目录中没有文件')
        while len(os.listdir(dir)) >= 100:
            try:
                lists = os.listdir(dir)
                lists.sort(key=lambda fn: os.path.getmtime(dir + '/' + fn))
                file_old0 = os.path.join(lists[0])
                file_old1 = os.path.join(lists[1])
                # 返回最早生成的文件名称
                log.debug('remove report file：%s' % file_old0)
                log.debug('remove report file：%s' % file_old1)
                os.remove(cls.dir + file_old0)
                os.remove(cls.dir + file_old1)
            except Exception as msg:
                log.error(msg)
                raise msg


    @classmethod
    def new_report_nopath(cls,reportpath):
        """
        对test_report目录中文件进行排序，返回最新生成的html文件
        :param reportpath:
        :return:
        """
        lists = os.listdir(reportpath)
        lists.sort(key=lambda fn: os.path.getmtime(reportpath + '/' + fn))
        if not os.listdir(reportpath):
            log.debug(u'目录中没有文件')
        elif lists[-1] == ".DS_Store":
            file_new = os.path.join(lists[-2])
        else:
            file_new = os.path.join(lists[-1])
        return file_new

    @classmethod
    def new_report_path(cls, reportpath):
        """
        对test_report目录中文件进行排序，返回最新生成的html文件
        :param reportpath:
        :return:
        """
        lists = os.listdir(reportpath)
        lists.sort(key=lambda fn: os.path.getmtime(reportpath + '/' + fn))
        if not os.listdir(reportpath):
            log.debug(u'目录中没有文件')
        elif lists[-1] == ".DS_Store":
            file_new = reportpath+os.path.join(lists[-2])
        else:
            file_new = reportpath+os.path.join(lists[-1])
        return file_new

    @classmethod
    def move_file(cls, oldpath, newpath):
        """
        移动文件到目标路径
        :param oldpath:
        :param newpath:
        :return:
        """
        try:
            shutil.move(oldpath, newpath)
        except BaseException as msg:
            print msg

    @classmethod
    def copy_file(cls, filepath, newpath):
        """
        复制指定文件到目标目录;
        :param filepath:
        :param newpath:
        :return:
        """
        try:
            shutil.copy(filepath, newpath)
            log.debug(u'copy=>ok')
        except BaseException as msg:
            print msg

    @classmethod
    def mkdir(cls, path='../Output/', name=None):
        """
        路径中存在name,则do nothing;
        路径中不存在name,则新建name;
        :param path:
        :param name:
        :return:
        """
        try:

            new_dirname = name
            new_path = os.path.join(path, new_dirname)
            if not os.path.isdir(new_path):
                os.makedirs(new_path)
                log.debug(u'创建文件夹成功'+str(new_path))
        except Exception as msg:
            log.debug(u'创建文件夹失败')
            print msg
            raise

    @classmethod
    def move_screenshot(cls, tarpath="Fail||Pass"):
        """
        移动截图到指定dirname目录中
        :return:tarpath = Fail||Pass
        """
        try:
            dirname = datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
            old_path = Os.ABSpath()+"/Output/Screenshot/"+tarpath+"/"
            path = Os.ABSpath()+"/Output/Screenshot/"
            new_path_screen = path+dirname
            for root, dirs, files in os.walk(old_path):
                if len(files) != 0:
                    Os.mkdir(old_path, new_path_screen)
                    log.debug(u'创建新路径')
                else:
                    log.debug(u'当前目录无文件，不创建新目录')
                if len(dirs) == 0:
                    for i in range(len(files)):
                        log.debug(u'查找file')
                        if files[i][-3:] == 'png':
                            log.debug(u'查找.png图片')
                            old_path_file = old_path+"/"+files[i]
                            new_path_screen_file = new_path_screen+"/"+files[i]
                            shutil.move(old_path_file, new_path_screen_file)
                            log.debug(u'执行移动')
                        else:
                            log.debug(u'当前路径无.png图片')
            log.debug(u'移动截图成功')
        except Exception as msg:
            log.error(u'移动截图失败')
            print msg
            raise

    @classmethod
    def del_screen(cls, who=" None||Fail||Pass"):
        """
        删除全部截图
        :param who:  None||Fail||Pass
        :return:
        """
        try:
            FalseScreenshotPath = readConfig(Config_path)['path']['FalseScreenshot']
            TrueScreenshotPath = readConfig(Config_path)['path']['TrueScreenshot']
            Os.mkdir(Os.ABSpath()+"/Output/Screenshot", "Fail")
            Os.mkdir(Os.ABSpath()+"/Output/Screenshot", "Pass")
            if who == "Fail":
                Os.del_file(dir=FalseScreenshotPath, filename='l')
            elif who == "Pass":
                Os.del_file(dir=TrueScreenshotPath, filename='l')
            else:
                Os.del_file(dir=FalseScreenshotPath, filename='l')
                Os.del_file(dir=TrueScreenshotPath, filename='l')
        except Exception as msg:
            log.error(u'删除截图失败')
            print msg
            raise

class Cookie(Operation):
    """
    cookie全部操作
    get_cookies（） 获得cookie信息
    add_cookie(cookie_dict)  向cookie添加会话信息
    delete_cookie(name)   删除特定(部分)的cookie
    delete_all_cookies()    删除所有cookie
    """

    @classmethod
    def get_cookie(cls):
        """获取cookie"""
        try:
            driver = cls.driver
            cookie = driver.get_cookies()
            if cookie != '':
                return cookie
            else:
                raise Exception
        except Exception as msg:
            log.error(u'获取cookie失败')
            print msg
            raise

    @classmethod
    def delete_all_cookie(cls):
        """删除所有cookie"""
        try:
            driver = cls.driver
            return driver.delete_all_cookies()
        except Exception as msg:
            log.error(u'获取cookie失败')
            print msg
            raise

    @classmethod
    def delete_cookie(cls, name):
        """删除所有cookie"""
        try:
            driver = cls.driver
            return driver.delete_cookie(name)
        except Exception as msg:
            log.error(u'获取cookie失败')
            print msg
            raise



