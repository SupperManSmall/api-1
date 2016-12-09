# coding=utf-8
__author__ = 'xcma'
import MySQLdb
import MySQLdb.cursors
from ReadConfig import readConfig
from Utils import ABSpath
import sys, time, Run, platform
from LogMainClass import Log
reload(sys)
sys.setdefaultencoding('utf-8')

log = Log('MySql')
url_target = Run.url_target
class MySQL:
    """
    mysql相关方法
    connect:链接数据库
    creat_table:创建表
    create datebase dbname；
    """

    @classmethod
    def connect(cls, database='', who='Null'):
        # 链接数据库
        conf_path = ABSpath() + '/Src/Conf/Config.yml'
        if who in 'short_url':
            mysql = readConfig(conf_path)['short_url']
        else:
            mysql = readConfig(conf_path)['local_mysql']
            if platform.system() == 'Linux':
                mysql = readConfig(conf_path)['xxtao_mysql']
        ip = mysql['ip']
        username = mysql["username"]
        password = mysql["password"]
        if not database:
            database = mysql["database"]
        try:
            db = MySQLdb.connect(
                ip, username, password, database, charset='utf8',  cursorclass=MySQLdb.cursors.DictCursor)
            log.debug(db)
            return db, db.cursor()
        except Exception as msg:
            raise msg

    @classmethod
    def command_line(cls, database, sql):
        try:
            db, cursor = MySQL.connect(database=database)
            cursor.execute(sql)
            # data = cursor.fetchone()
            # data = cursor.fetchmany(a)
            data = cursor.fetchall()
            # 执行数据入库
            db.commit()
            return data
        except Exception as msg:
            raise msg
        finally:
            # 关闭数据库连接
            cursor.close()
            db.close()

    @classmethod
    def create_table(cls, database, table_name):
        try:
            db, cursor = MySQL.connect(database=database)
            sql = """
            CREATE TABLE """+table_name+""" (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `if_name` varchar(10) Not Null comment '接口名称',
              `case_name` varchar(20) comment '用例名称',
              `status` varchar(5),
              `result` varchar(20),
              `response` varchar(1000),
              `url_target` varchar(20) comment '执行域名',
              `comment` varchar(30),
              `type` varchar(10) comment '执行接口类型',
              `uptm` timestamp not null,
              PRIMARY KEY (`id`)
            ) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
            """

            cursor.execute(sql)
            data = cursor.fetchone()
            # 执行数据入库
            db.commit()
            return data
        except Exception as msg:
            raise msg
        finally:
            # 关闭数据库连接
            db.close()

    @classmethod
    def drop_table(cls, database, tablename):
        try:
            db, cursor = MySQL.connect(database=database)
            sql = "DROP TABLE IF EXISTS "+tablename+";"
            cursor.execute(sql)
            data = cursor.fetchone()
            db.commit()
            return data
        except Exception as msg:
            raise msg
        finally:
            db.close()

    @classmethod
    def insert(cls, if_name, case_name, comment, status='0', result='Fail', response='Null', table_name='test_result'):

        try:
            uptm = MySQL.get_now_time()
            type = Run.Main
            db, cursor = MySQL.connect()
            # 使用cursor()方法获取操作游标
            # 写sql
            sql1 = '''SET NAMES 'UTF8';'''
            sql = "INSERT INTO "+table_name+" (if_name, case_name, url_target, comment, type, uptm, status, result, response) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)"
            # 使用execute方法执行SQL语句
            cursor.execute(sql1)
            cursor.execute(sql, [if_name, case_name, url_target, comment, type, uptm, status, result, response])
            # 获取执行结果
            data = cursor.fetchone()
            # 执行数据入库
            db.commit()
            log.debug('Insert table OK')
            return data
        except Exception as msg:
            raise msg
        finally:
            # 关闭数据库连接
            db.close()

    @classmethod
    def insert_by_sql(cls, sql):

        try:
            db, cursor = MySQL.connect()
            # 使用cursor()方法获取操作游标
            # 写sql
            sql1 = '''SET NAMES 'UTF8';'''
            # 使用execute方法执行SQL语句
            cursor.execute(sql1)
            cursor.execute(sql)
            # 获取执行结果
            data = cursor.fetchone()
            # 执行数据入库
            db.commit()
            log.debug('Insert table OK')
            return data
        except Exception as msg:
            raise msg


    @classmethod
    def update(cls, database, table_name, city_id, city_name, city_index):
        try:
            db, cursor = MySQL.connect(database=database)
            # 使用cursor()方法获取操作游标
            # 写sql
            sql1 = '''SET NAMES 'UTF8';'''
            sql = "update `"+table_name+"` set `city_id`="+city_id+",`city_name`='"+city_name+"', `city_index` ='"+city_index+"' where city_id="+city_id+""
            # log.debug(sql)
            # 使用execute方法执行SQL语句
            cursor.execute(sql1)
            cursor.execute(sql)
            # 获取执行结果
            data = cursor.fetchone()
            # 执行数据入库
            db.commit()
            return data
        except Exception as msg:
            raise msg
        finally:
            # 关闭数据库连接
            db.close()

    @classmethod
    def get_now_time(cls):
        """
        获取当前时间，格式为：YY:MMM:DD HH:MM:SS
        :return:
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    @classmethod
    def query(cls, database, sql, who='Null'):
        """
        查询表，且带上字段名称
        :param database:输入表名
        :param sql:输出查询语句
        :return:返回字典
        """
        try:
            db, cur = MySQL.connect(database=database, who=who)
            cur.execute(sql)
            index = cur.description
            result = []
            response = cur.fetchall()
            if response:
                for res in response:
                    row = {}
                    for i in range(len(index) - 1):
                        row[index[i][0]] = res[index[i][0]]
                    result.append(row)
                db.close()
                return result
            else:
                return {'status': '0', 'msg': 'result is Null'}
        except Exception as msg:
            print (msg)
            raise

    @classmethod
    def del_table(cls, table_name, database='god'):
        try:
            if 'xx' not in url_target:
                url = 'wan%'
            else:
                url = 'xx%'
            db, cursor = MySQL.connect(database=database)
            sql = """
                delete from """+table_name+""" where url_target like'"""+url+"""';
            """
            sqlq = """
                ALTER TABLE %s auto_increment=1;
            """ % table_name
            cursor.execute(sql)
            cursor.execute(sqlq)
            data = cursor.fetchone()
            # 执行数据入库
            db.commit()
            return data
        except Exception as msg:
            print (msg)
            raise

    @classmethod
    def get_test_result(cls):
        try:
            sql = "select * from test_result order by if_name;"
            test_result = MySQL.query('god', sql)
            return test_result
        except Exception as msg:
            print (msg)
            raise

    @classmethod
    def set_test_result(cls, response, status_code, interfacename, casename, comment, result):
        status = ''
        try:
            status = response['succ']
            cls.response_new = 'succ:%s' % response['succ']
            try:
                if response['succ'] != '1':
                    # 有可能不存在msg，try一下
                    cls.response_new = response['msg']
            except:
                pass
        except:
            status = status_code
            cls.response_new = MySQL.todo_string(response)
        finally:
            try:
                MySQL.insert(interfacename, casename, comment, status, result, cls.response_new)

            except Exception as msg:
                print (msg)
                raise

    @classmethod
    def set_test_result_ui(cls, case_name, short_url_id, short_tag, comment, status, result):
        """
        插入ui测试用例执行结果
        :param response:
        :param status_code:
        :param interfacename:
        :param casename:
        :param comment:
        :param result:
        :param table_name: 指定表名
        :return:
        """
        uptm = MySQL.get_now_time()
        type = Run.Main
        try:
            sql = """INSERT INTO test_short_url (
                      case_name,short_url_id,short_tag,result,status,url_target,comment,type,uptm)
                      VALUE ('""" + case_name + """','""" + str(short_url_id) + """','""" + str(
                short_tag) + """','""" + result + """','""" + str(status) + """','""" + url_target + """','""" + str(
                comment) + """','""" + type + """','""" + uptm + """');"""
            MySQL.insert_by_sql(sql)
        except Exception as msg:
            print (msg)
            raise

    @classmethod
    def todo_string(cls, string):
        """
        返回值response为字符串时调用此方法
        :param string:
        :return:
        """
        return string.replace('\n', '').replace(' ', '')[0:20]

    @classmethod
    def select_short_url(cls):
        """
        查询short_url表 中数据
        :return:
        """
        if 'xx' not in url_target:
            like = 'http://m.wanpinghui.com/%'
        else:
            like = 'http://m.xxtao.com/%'
        try:
            sql = "SELECT * FROM short_url where short_url like '"+like+"' ORDER BY short_url_id DESC LIMIT 1;"
            select_result = MySQL.query(database='db_short_url', sql=sql, who='short_url')[0]
            log.debug("select_result:")
            log.debug(select_result)
            return select_result
        except Exception as msg:
            print (msg)
            raise