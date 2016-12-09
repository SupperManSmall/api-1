# coding=utf-8
__author__ = 'xcma'

import os
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from LogMainClass import Log
from ReadConfig import readConfig
from Utils import ABSpath
import smtplib, Run
import GlobalVariable
log = Log("Email.py")
def send_mail(send_file_path, send_who):
    """
    :param send_file_path: 测试报告文件路径
    :return:
    """
    title = ''
    Main = Run.Main
    input_url = Run.url_target
    config_file_path = ABSpath()+"/Src/Conf/Config.yml"
    email = readConfig(config_file_path)['email']
    smtpserver = email['mail_host']
    smtpuser = email['mail_user']
    password = email['mail_pass']
    mailto = []
    try:
        if send_who == "Null":
            #拼装接收人
            if input_url in 'www.wanpinghui.com':
                receive_category = "email_receiver_wph"
                mailto = readConfig(config_file_path)[receive_category]
            elif input_url in 'www.xxtao.com':
                receive_category = "email_receiver_xxtao"
                mailto = readConfig(config_file_path)[receive_category]
        else:
            mailto = send_who
        log.debug("send_file_path：%s" % send_file_path)
        log.debug("smtpserver：%s" % smtpserver)
        log.debug("smtpuser：%s" % smtpuser)
        log.debug("password：%s" % password)
        log.debug("mailto:%s" % mailto)
        msg = MIMEMultipart()
        #定义发送人
        msg['From'] = smtpuser

        #定义接收邮件对象
        msg['To'] = ",".join(mailto)

        #邮件标题
        run_case_total, run_pass_total, run_failures_total, run_error_total = GlobalVariable.parsing_string(GlobalVariable.get_value())
        title = "["+str(input_url)+"|C:"+str(run_case_total)+"|P:"+str(run_pass_total)+"|F:"+str(run_failures_total)+"|E:"+str(run_error_total)+"]"
    except Exception as msg:
        raise msg

    if 'u' in Main:
        Subject = "%sUI_Report" % title
    else:
        Subject = "%sAPI_Report" % title

    times = GlobalVariable.get_times()
    if times in [49, 50]:
        Subject1 = "=>System_Push"
    else:
        Subject1 = ''
    Subject = Subject+Subject1
    msg['Subject'] = Header(Subject, 'utf-8').encode()
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"

    file_name = new_report(send_file_path)
    sendfile = send_file_path + file_name

    content1 = """<h3><a href = "http://pages.wph.xxtao.com/test-report/"""+file_name+""""">在线报告</a>||<a href = "http://at.test.xxtao.com/">实时监控系统</a><h3>"""
    content2 = "<h3>测试环境：[" + input_url + "] <h3>"
    content = content1+content2
    fp = open(sendfile, 'rb')
    try:
        # 将html中内容贴在邮件正文中
        msg.attach(MIMEText(content+fp.read(), 'html', 'utf-8'))
    except Exception as msg:
        log.error(u'邮件发送失败')
        raise msg
    finally:
        fp.close()

        # 添加附件
        fp = open(sendfile, 'rb')
    try:
        part = MIMEApplication(fp.read())
        part.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(part)
    except Exception as msg:
        log.error(u'邮件发送失败')
        raise msg
    finally:
        fp.close()

    try:
        # 发送邮件
        server = smtplib.SMTP()
        try:
            #不加密形式
            server.connect(smtpserver, '25')
        except:
            # 通过ssl形式发送邮件
            server = smtplib.SMTP_SSL(smtpserver, '465')

        #log.debug(u'邮件日志'+str(server.set_debuglevel(1)))
        server.login(smtpuser, password)
        server.sendmail(smtpuser, mailto, msg.as_string())
        server.quit()
        log.debug(u'邮件发送成功')
    except Exception as msg:
        log.error(u'邮件发送失败')
        raise msg
def new_report(testreport):
    '''
    将文件按照名字时间顺序排序,输出文件名字
    :param testreport:测试报告存放路径
    :return:
    '''

    try:
        lists = os.listdir(testreport)
        log.debug(u'当前路径中文件列表'+str(lists))
        lists.sort(key=lambda fn: os.path.getmtime(testreport + '/' + fn))
        file_new = os.path.join(lists[-1])
        #返回最新生成的文件名称
        log.debug(u'将要发送的测试报告文件：'+file_new)
        return file_new
    except Exception as msg:
        raise msg

def sendemail(test_Report_path):
    # 第20次执行用例，主动报告测试情况

    try:
        value = GlobalVariable.get_value()
    except:
        log.error(u"Runner fail =》Report.py,result error")
    run_case_total, run_pass_total, run_failures_total, run_error_total = GlobalVariable.parsing_string(value)
    log.warning("run_case_total:%s" % str(run_case_total))
    log.warning("run_error_total:%s" % str(run_error_total))
    log.warning("run_failures_total:%s" % str(run_failures_total))
    log.warning("run_pass_total:%s" % str(run_pass_total))

    sendemail = Run.email
    send_who = Run.send_who
    times = GlobalVariable.get_times()
    log.debug("times:%s" % times)

    send_msg = 'send_email=> fail'
    send_mail_msg = 'send_email=> No'

    if sendemail in 'true':
        try:
            send_mail(test_Report_path, send_who)
        except Exception as msg:
            log.error(send_msg)
            log.error(msg)
            raise msg

    elif sendemail in 'misc':
        if times in [49, 50]:
            try:
                send_mail(test_Report_path, send_who)
            except Exception as msg:
                log.error(send_msg)
                log.error(msg)
                raise msg

        elif run_error_total != '0' or run_failures_total != '0':
            try:
                send_mail(test_Report_path, send_who)
            except Exception as msg:
                log.error(send_msg)
                log.error(msg)

        elif send_who != 'Null':
            try:
                send_mail(test_Report_path, send_who)
            except Exception as msg:
                log.error(send_msg)
                log.error(msg)
                raise msg
        else:
            log.warning(send_mail_msg)
    else:
        log.warning(send_mail_msg)