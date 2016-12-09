# coding=utf-8
__author__ = 'xcma'
import os,sys,Run


ABSPATH = os.path.abspath(sys.argv[0])
ABSPATH = os.path.dirname(ABSPATH)

#将代码备份到../backup文件夹下
parameter = Run.backup
pas = ["t", "tyue"]
if parameter in pas:
    new_dirname = 'God_gitHub'
    creat_path = '../'
    backup_path = creat_path+new_dirname
    try:

        new_path = os.path.join(creat_path, new_dirname)
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        # command1 = 'ls'
        # os.system(command1)
        # os.system('pwd')
        command = "cp -r "+ABSPATH+"/* "+backup_path
        os.system(command)
        print u'代码库备份成功'
    except:
        print u'代码库备份失败'
