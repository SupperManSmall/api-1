# coding=utf-8
__author__ = 'xcma'

import ConfigParser
import yaml

def readConfig(path):
    try:
        f = open(path)
        dataMap = yaml.load(f)
        return dataMap
    except Exception as msg:
        raise msg
    finally:
        f.close()


