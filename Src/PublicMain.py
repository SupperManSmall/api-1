# coding=utf-8
__author__ = 'xcma'
from Function.Report import MainRelated
from Function.LogMainClass import Log
from Function.ReadConfig import readConfig
from Function.UiMethods import Os
from Function.MySql import MySQL
import platform
from Function import GlobalVariable
from Function.Email import sendemail
from Function.ApiMethod import Api_urllib
import time, Run


# 实例化日志
log = Log('PublicMain.py')
starttime = time.time()
log.debug(u"start_time:%s" % time.strftime('%Y-%m-%d %X', time.localtime(starttime)))
log.debug("########### start ###########")
#读取配置信息
Config_path_ym = Os.ABSpath() + "/Src/Conf/Config.yml"
read_test_dir = readConfig(Config_path_ym)['path']['test_dir']
read_global_dir = readConfig(Config_path_ym)['path']['global_dir']
read_test_report = readConfig(Config_path_ym)['path']['test_report']
read_send_report = ''
if platform.system() == 'Windows':
    read_send_report = readConfig(Config_path_ym)['path']['send_report']
elif platform.system() == 'Darwin' or platform.system() == 'Linux':
    read_send_report = readConfig(Config_path_ym)['path']['send_report']

# 清空数据库
# m = Run.Main
# if m in 'api':
#     MySQL.del_table('test_result')

# test_dir    : 用例执行目录
test_dir = Os.ABSpath() + read_test_dir
Os.mkdir(path=Os.ABSpath() + '/Output', name="Testdir")
log.debug('test_dir:%s' % test_dir)

# global_dir  : 存放中间数据的文件夹
global_dir = Os.ABSpath() + read_global_dir
Os.mkdir(path=Os.ABSpath() + '/Output', name="Global")
log.debug('global_dir:%s' % global_dir)

# 统计主程序执行次数
GlobalVariable.set_times()

# 提前清空执行目录
Os.del_file(dir=test_dir, filename='l')
log.debug('remove_testdir=>ok')

# test_report_path :  测试报告存放
test_Report_path = Os.ABSpath() + read_test_report
Os.mkdir(path=Os.ABSpath() + "/Output", name='TestReport')
log.debug('test_Report_path:%s' % test_Report_path)

# send_Report_path  :   根据系统指定不同发送保存存放路径
send_Report_path = Os.ABSpath() + read_send_report
Os.mkdir(path=Os.ABSpath() + "/Output", name='SendReport')
log.debug('send_Report_path:%s' % send_Report_path)

# 生成测试报告，并运行用例
try:
    MainRelated.generate_case_suite(test_dir)
    MainRelated.generate_report(test_dir, test_Report_path)
except:
    msg = 'PublicMain.py [line 64]=>Fail'
    log.error(msg)
    raise msg
# # 输出测试情况
# MainRelated.generate_test_result()

#根据demand_id删除需求
if not Run.run_case:
    try:
        demand_id_read = Api_urllib.read_from_file()
        for demand_id in demand_id_read:
            log.debug(demand_id)
            Api_urllib.del_demand(demand_id)
        # file_path = Os.ABSpath() + readConfig(Config_path_ym)['path']['global_dir']
        # file_name = 'demand_id'
        # Os.del_file_specific(file_path, file_name)
    except Exception as msg:
        log.warning(msg)

# 删除执行目录中的用例
try:
    delete_TestDir = "yes"
    if delete_TestDir == 'yes':
        Os.del_file(dir=test_dir, filename='l')
        log.debug('remove=>ok')
    else:
        log.debug('remove=>No')
except:
    msg = u'操作执行目录失败'
    log.error(msg)
    raise msg

# 将测试报告移到发送目录中
# try:
#     fn = Os.new_report_path(test_Report_path)
#     fin = Os.new_report_nopath(test_Report_path)
#     Os.del_file(dir=send_Report_path, filename=fin)
#     Os.copy_file(fn, send_Report_path)
#     log.debug(u'将测试报告移到发送目录中成功')
# except:
#     msg = u'将测试报告移到发送目录中失败'
#     log.error(msg)
#     raise msg

# 发送邮件
sendemail(test_Report_path)

# 删除TestReport中文件
try:
    delete_report = Run.del_report
    if delete_report in 'true':
        Os.del_file_the_earliest(dir=test_Report_path)
        log.debug('remove TestReport=>ok')
    else:
        log.debug('remove TestReport=>No')
except:
    msg = u'操作TestReport中文件失败'
    log.error(msg)
    raise msg

log.debug('########### Done ###########')
stoptime = time.time()
dotime = stoptime - starttime
log.debug("end_time:%s" % time.strftime('%Y-%m-%d %X', time.localtime(stoptime)))
log.debug('execution time：%.2fS' % dotime)