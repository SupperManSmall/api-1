# coding=utf-8
__author__ = 'xcma'

import os, sys, getopt, string, json
from Src.Function.Utils import *
from Src.Function.ReadConfig import readConfig

# utf-8
reload(sys)
sys.setdefaultencoding('utf8')

msg = "ParameterError:参数错误，You can get help in this way:[-h]"

# 若依赖的binary文件放在系统PATH下(如/usr/local/bin)，1. 安装起来比较分散，2. 因权限等出了毛病难定位
# 故，放在当前目录的bin下，用脚本自动安装
os.environ["PATH"] += (os.pathsep + ABSpath() + '/bin')

Init_config_path_ym = ABSpath() + "/Src/Conf/InitParameter.yml"
value_all = readConfig(Init_config_path_ym)['value_all']

# 读value
level_value = value_all['level_value']
brower_value = value_all['brower_value']
report_value = value_all['report_value']
del_value = value_all['del_value']
backup_value = value_all['backup_value']
Main_value = value_all['Main_value']
email_value = value_all['email_value']
send_email_value = value_all['send_email_value']
url_value = value_all['url_value']
case_whitch_value = value_all['case_whitch_value']
# 初始值设置：
environment = readConfig(Init_config_path_ym)['Environment']['environment']
category_local = "Local"
category_production = "Production"
category = ""
if environment in category_local:
    print ("""本地环境""")
    category = category_local

elif environment in category_production:
    print ("""部署环境""")
    category = category_production

config = readConfig(Init_config_path_ym)[category]
log = config['log']
brower = config['brower']
report = config['report']
del_report = config['del_report']
backup = config['backup']
Main = config['Main']
email = config['email']
send_who = config['send_who']
url_target = config['url_target']
run_case = config['run_case']
all_case_name = config['all_case_name']
run_case_by_filename = config['run_case_by_filename']
# 读取全部可执行用例名称
ApiCaseSummary_path_ym = ABSpath() + "/Src/Conf/ApiCaseSummary.yml"
ApiCaseSummary = json.dumps(readConfig(ApiCaseSummary_path_ym), indent=4)

def usage():
    """使用说明"""
    print (url_target)
    print ("""
    参数使用说明:
        -l  [ info   || debug  || error    || warning]
        -b  [ chrome || firfox || phantomjs]
        -m  [ ui     || api    || excel    ]
        -r  [ true   || false  ]
        -d  [ true   || false  ]
        -u  [ true   || false  ]
        -e  [ true   || false  || misc     ]
        -s  [ XX@163.com       ]
        -t  [ xxtao  || wanpinghui    ]
        -c  [ a01      ]
        -n  [ test_a.py        ]
    !**
        -l: log        default: """ + log + """
        -b: brower     default: """ + brower + """
        -m: Main                default: """ + Main + """
        -r: report              default: """ + report + """
        -d: del_report          default: """ + del_report + """
        -t: url_target          default: """ + url_target + """
        -u: backup              default: """ + backup + """
        -e: email               default: """ + email + """
        -s: send_email          default: """ + send_who + """
        -t: url_target          default: """ + url_target + """
        -c: run_case_shortname  default: """ + run_case + """
        -n: run_case_file_name  default: """ + run_case_by_filename + """
    eg: python Run.py -l info -b chrome -r true

    """)


# 拼装传入参数列表
ParameterSummary = value_all['ParameterSummary']
summary = ParameterSummary + level_value + brower_value + report_value + del_value + Main_value + send_email_value \
          + url_value + email_value + case_whitch_value
ValueSummary = level_value + brower_value + report_value + del_value + Main_value + send_email_value + url_value \
               + email_value + case_whitch_value

# 检查传入参数是否正确
inputparameter = []
for i in range(1, len(sys.argv)):
    parameter = sys.argv[i]
    inputparameter = inputparameter + [parameter]
# print inputparameter
    # if parameter not in summary:
    #     print ('input:'+msg)
    #     sys.exit()

# 参数设置，必须在参数后面添加冒号，如果不加冒号则对应的参数值会进入到args[]中
opts, args = getopt.getopt(sys.argv[1:], 'hl:b:r:d:u:m:s:e:t:c:n:')
# print ("opts%s" % opts)
# print ("args %s" % args)
# sys.exit()
"""说明：参数h为开关，l：为日志级别输出参数；如果新增p参数，则可以'hl:p:'这样写"""
if '-h' not in inputparameter and sys.argv == []:
    if not opts:
        print ('-h:' + msg)
        sys.exit()

# url_target
for op, value in opts:
    if op == '-t':
        if value in url_value:
            url_target = value
        else:
            print ('url_target:' + msg)
            sys.exit()
    elif op == '-h':
        usage()
        sys.exit()

# log
for op, value in opts:
    if op == '-l':
        if value in level_value:
            log = value
        else:
            print ('level:' + msg)
            sys.exit()
    elif op == '-h':
        usage()
        sys.exit()

# brower
for op, value in opts:
    if op == '-b':
        if value in brower_value:
            brower = value
        else:
            print ('brower:' + msg)
            sys.exit()
    elif op == '-h':
        usage()
        sys.exit()

# report
for op, value in opts:
    if op == '-r':
        if value in report_value:
            report = value
        else:
            print ('report:' + msg)
            sys.exit()
    elif op == '-h':
        usage()
        sys.exit()

# del_report
for op, value in opts:
    if op == '-d':
        if value in del_value:
            del_report = value
        else:
            print ('del_report:' + msg)
            sys.exit()
    elif op == '-h':
        usage()
        sys.exit()

# backup
name = 'backup:'
for op, value in opts:
    if op == '-u':
        if value in backup_value:
            backup = value
        else:
            print (name + msg)
            sys.exit()
    elif op == '-h':
        usage()
        sys.exit()

# Main 执行哪种测试
whichMain = 'Main:'
for op, value in opts:
    if op == '-m':
        if value in Main_value:
            Main = value
        else:
            print (whichMain + msg)
            sys.exit()
    elif op == '-h':
        usage()
        sys.exit()

# email
If_email = 'Email:'
for op, value in opts:
    if op == '-e':
        if value in email_value:
            email = value
        else:
            print (If_email + msg)
            sys.exit()
    elif op == '-h':
        usage()
        sys.exit()

# receive_name
receive_name = 'Email:'
for op, value in opts:
    if op == '-s':
        if value in send_email_value:
            send_who = value
        else:
            print (receive_name + msg)
            sys.exit()
    elif op == '-h':
        usage()
        sys.exit()

# 指定运行case， value
run_case_name = 'case_name:'
for op, value in opts:
    if op == '-c':
        if ',' not in value:
            run_case = value
        else:
            run_case = value.split(',')
    elif op == '-h':
        usage()
        sys.exit()


# 通过用例文件名进行测试
for op, value in opts:
    if op == '-n':
        if ',' not in value:
            run_case_by_filename = value
        else:
            run_case_by_filename = value.split(',')
    elif op == '-h':
        usage()
        sys.exit()

import Src.PublicMain