# coding=utf-8
__author__ = 'xcma'
import datetime, unittest, ConfigParser, Run
from Src.Lib.HTMLTestRunner import HTMLTestRunner
from ReadConfig import readConfig
from UiMethods import Os
from LogMainClass import Log
from MySql import MySQL
import GlobalVariable,os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

log = Log('MainRelated')
#获取传参
report = Run.report
Main = Run.Main
url_target = Run.url_target
run_case = Run.run_case
run_case_by_name = Run.run_case_by_filename
# run_case = ['a05', 'c01']
log.debug('run_case: %s' % run_case)
class MainRelated():
    u'''为构造测试用例、目录、套件服务'''
    log.debug('MainRelated=》start')

    @classmethod
    def generate_report(cls, test_dir, test_Report_path):
        """
        主套件执行方法
        :param test_dir:
        :param test_Report_path:
        :return:
        """
        try:
            test_dir = str(test_dir)
            test_Report_path = str(test_Report_path)
            now = datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-4]
            filename = test_Report_path + now + '_report.html'
            fp = open(filename, 'wb')
            if report in 'true' or report == '':
                name = ''
                if Main in 'ui':
                    name = "UI Automated test report"
                elif Main in 'api':
                    name = "API Automated test report"
                # 定义测试报告
                runner = HTMLTestRunner(stream=fp,
                                        title=name,
                                        description='General situation of testcase')
                log.debug(u'BY=>HtmlTestRunner')
            elif report in 'false':
                runner = unittest.TextTestRunner()
                log.debug('BY=>Unittest')

            # 控制执行路径
            result = '<unittest.runner.TextTestResult run=0 errors=0 failures=0>'
            if os.listdir(test_dir):
                discover = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')
                r = runner.run
                result = r(discover)
                log.debug(result)
            else:
                log.warning(u'test_dir is empty')

            # 传递运行结果
            GlobalVariable.set_value(result, report)
        except Exception as msg:
            log.error(u'Runner=》ERROR')
            raise msg

        finally:
            fp.close()

    @classmethod
    def shortNameToFileName(cls):
        log.warning('run_case:%s' % run_case)
        # 指定哪个平台的用例
        case_platform = Run.Main
        if case_platform in 'api':
            CaseSummary_path = Os.ABSpath() + "/Src/Conf/ApiCaseSummary.yml"
        else:
            CaseSummary_path = Os.ABSpath() + "/Src/Conf/UiCaseSummary.yml"

        # 找到指定平台的用例集
        run_case_name = []
        main_case = []
        case_summary = readConfig(CaseSummary_path)
        if case_summary:
            for key, value in case_summary.items():
                case_summary_part = readConfig(CaseSummary_path)[key]
                # 若case_summary_part 为空时，略过
                try:
                    for x, y in case_summary_part.items():
                        # 找到所有用例简称 a01， 如果与传参相等则返回该用例文件名
                        if type(run_case) != list:
                            if run_case in x:
                                log.debug(y)
                                return y, key
                        elif type(run_case) == list:
                            for q in range(0, len(run_case)):
                                if run_case[q] in x:
                                    run_case_name.append(y)
                                    main_case.append(key)
                except:
                    pass
            log.debug('run_case_name: %s' % run_case_name)
            log.debug('main_case: %s' % main_case)
            return run_case_name, main_case

    @classmethod
    def move_case(cls, main_case_path, case_name, test_dir):
        """
        移动case文件
        :param main_case_path:
        :param case_name:
        :param test_dir:
        :return:
        """
        if type(main_case_path) == list:
            for path in main_case_path:
                # 寻找将执行用例的文件名称
                log.debug('case_name:%s' % case_name)
                find_case_path = Os.ABSpath() + path
                # 寻找将执行用例的路径
                log.debug('find_case_path:' + str(find_case_path))
                case_path = find_case_path + case_name
                # 找到要执行的用例文件路径
                log.debug('case_path:' + str(case_path))
                Os.copy_file(case_path, test_dir)
        else:
            log.debug('case_name:%s' % case_name)
            find_case_path = Os.ABSpath() + main_case_path
            # 寻找将执行用例的路径
            log.debug('find_case_path:' + str(find_case_path))
            case_path = find_case_path + case_name
            # 找到要执行的用例文件路径
            log.debug('case_path:' + str(case_path))
            Os.copy_file(case_path, test_dir)

    @classmethod
    def generate_case_suite(cls, test_dir):
        """
        1.读取用例集配置文件，并将需要执行的用例复制到执行目录中
            who = ui / api
        2.根据传入参数run_case，将制定用例移入test_dir文件夹中
        :param test_dir:
        :return:
        """
        Config_path = Os.ABSpath() + "/Src/Conf/Config.yml"
        try:
            test_dir = str(test_dir)
            casesummartLocalpath = ''
            category = ''
            main_path = []
            case = []
            main_case_path = ''
            if Main in'ui':
                casesummartLocalpath = "/Src/Conf/UiCaseSummary.yml"
                category = "UiCase"
            elif Main in 'api':
                casesummartLocalpath = "/Src/Conf/ApiCaseSummary.yml"
                category = "ApiCase"
            CaseSummary_path = Os.ABSpath() + casesummartLocalpath
            log.debug(u'CaseSummary_path：%s' % CaseSummary_path)
            case_main = readConfig(Config_path)[category]
            # 全部可执行用例集及相应路径=》case_main
            log.debug('case_main:%s' % case_main)
            if case_main:
                # 通过用例小名进行测试
                if run_case_by_name == '' and type(run_case_by_name) != list:

                    if type(run_case) != list and run_case in 'all':
                        for main_name, main_case_path in case_main.items():
                            case = readConfig(CaseSummary_path)[main_name]
                            try:
                                for case_key, case_name in case.items():
                                    MainRelated.move_case(main_case_path, case_name, test_dir)
                            except:
                                log.warning("%s is null" % main_name)
                    else:
                        # 通过main_name确定main_case_path的值
                        run_case_name, main_case = MainRelated.shortNameToFileName()
                        for main_name, main_case_path in case_main.items():
                            log.debug('main_name:%s' % main_name)
                            if main_name in main_case:
                                main_path.append(main_case_path)
                                log.debug('main_path:%s' % main_path)

                        if type(run_case_name) != list:
                            MainRelated.move_case(main_path, run_case_name, test_dir)
                        elif type(run_case_name) == list:
                            for case_name in run_case_name:
                                MainRelated.move_case(main_path, case_name, test_dir)

                # 通过用例文件名进行测试
                else:
                    for main_name, main_case_path in case_main.items():
                        case = readConfig(CaseSummary_path)[main_name]
                        log.debug('main_name:%s' % main_name)
                        log.debug('main_case_path:%s' % main_case_path)
                        log.debug('case:%s' % case)
                        casename = []
                        # 统计当前main_case_path下所有的casename
                        try:
                            for case_key, case_name in case.items():
                                casename.append(case_name)
                        except:
                            pass
                        if case:
                            if type(run_case_by_name) != list:
                                # run_case_by_name 为默认值是''：
                                if run_case_by_name == '':
                                    for case_key, case_name in case.items():
                                        MainRelated.move_case(main_case_path, case_name, test_dir)
                                else:
                                    # run_case_by_name为字符串，指定：单一用例文件
                                    for casename_value in casename:
                                        if casename_value == run_case_by_name:
                                            case_name = run_case_by_name
                                            MainRelated.move_case(main_case_path, case_name, test_dir)

                            # run_case 为列表时：
                            elif type(run_case_by_name) == list:
                                # 传参run_case与当前main_case_path路径下casename 进行对比
                                for run_case_name in run_case_by_name:
                                    for casename_value in casename:
                                        if casename_value == run_case_name:
                                            case_name = run_case_name

                                            # 如果存在相同casename，则替换执行用例为传入参数，并进行移动
                                            MainRelated.move_case(main_case_path, case_name, test_dir)

            else:
                log.warning('case_main is Null')
        except Exception as msg:
            log.error(u'generate_case_suite=》fail')
            raise msg

    @classmethod
    def generate_test_result(cls):
        """根据表里结果，遍历输出测试结果"""
        m = Run.Main
        try:
            if m in 'api':
                response = MySQL.get_test_result()
                # log.debug(response)
                # 收集case_name
                if_name = []
                for i in response:
                    if_name.append(i['if_name'])

                # 将case_name去重
                    if_name_one = []
                for x in if_name:
                    if x not in if_name_one:
                        if_name_one.append(x)

                    # 筛选出当前case_name的全部用例执行结果，若有一条失败则失败
                result = {}
                for if_name in if_name_one:
                    for i in response:
                        if url_target in i['url_target']:
                            if i['if_name'] == if_name:
                                if i['result'] == 'Fail':
                                    result[i['if_name']] = i['result']
                                    log.warning('ERROR==>>'+i['if_name']+'('+i['comment']+')'+':'+i['result']+
                                                '{status:"'+i['status']+'",response:"'+i['response']+'"}')
                                    break
                                else:
                                    log.warning(i['if_name'] + '(' + i['comment'] + ')' + ':' + i['result'])
                                    break
        except:
            pass
