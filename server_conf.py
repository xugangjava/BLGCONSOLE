# coding=utf-8
import os

PAY_CONFIG = [
    # 百乐宫
    {'id': 'icon_1', 'count': 300, 'price': 30, 'game_no': 'blg'},
    {'id': 'icon_2', 'count': 60, 'price': 6, 'game_no': 'blg'},
    {'id': 'icon_2', 'count': 60, 'price': 6, 'game_no': 'blg'},
    {'id': 'icon_3', 'count': 180, 'price': 18, 'game_no': 'blg'},
    {'id': 'icon_4', 'count': 680, 'price': 68, 'game_no': 'blg'},
    {'id': 'icon_5', 'count': 1280, 'price': 128, 'game_no': 'blg'},
    {'id': 'icon_6', 'count': 3280, 'price': 328, 'game_no': 'blg'},
    {'id': 'icon_7', 'count': 6480, 'price': 648, 'game_no': 'blg'},
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_HOST = "http://ggblg.billionocean.cn:8000/"
DEBUG = False 
DB_PWD='BMsCt8BNuRssYrkWB9c9'
PAY_DEBUG=False
IS_ENABLE_REAL_ITEM=1


import sitecustomize
if sitecustomize.CUR_SERVER_ADDRESS == "blgserver":
    # 百乐宫正式服务器
    WEB_HOST = "http://blgserver.billionocean.cn:8000/"
    DEBUG = False
    DB_PWD = 'BMsCt8BNuRssYrkWB9c9'
    PAY_DEBUG = False
elif sitecustomize.CUR_SERVER_ADDRESS == "ggblg":
    # 海外审核服务器
    WEB_HOST = "http://btserver.billionocean.cn:8000/"
    DEBUG = False
    DB_PWD = 'BMsCt8BNuRssYrkWB9c9'
    PAY_DEBUG = False
elif sitecustomize.CUR_SERVER_ADDRESS == "btserver":
    # 海外审核服务器
    WEB_HOST = "http://btserver.billionocean.cn:8000/"
    DEBUG = False
    DB_PWD = 'BMsCt8BNuRssYrkWB9c9'
    PAY_DEBUG = False
elif sitecustomize.CUR_SERVER_ADDRESS == "lffddzsrever":
    # 海外审核服务器
    WEB_HOST = "http://lffddz.billionocean.cn:8000/"
    DEBUG = False
    DB_PWD = 'gutG3vhsxBeYMSsUNUiblfddz'
    PAY_DEBUG = False
else:
    # 本机服务器
    WEB_HOST = "http://192.168.1.102:8000/"
    DEBUG = False
    DB_PWD = 'bo2016@'
    PAY_DEBUG = True


def LOG_INIT():
    import logging
    from logging.handlers import TimedRotatingFileHandler
    import re
    log_fmt = '%(asctime)s\t: %(message)s'
    formatter = logging.Formatter(log_fmt)
    log_file_path = os.path.join(BASE_DIR, 'log', "console.log")
    print "LOGPATH:" + log_file_path
    log_file_handler = TimedRotatingFileHandler(log_file_path, when="midnight")
    # log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
    #  log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
    log_file_handler.setFormatter(formatter)
    log_file_handler.setLevel(logging.NOTSET)
    log = logging.getLogger()
    log.setLevel(logging.NOTSET)

    log.addHandler(log_file_handler)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


LOG = LOG_INIT()

def TRACE(*args):
    try:
        data=str(''.join([str(a) for a in args])).encode('gbk').decode('gbk')
        if DEBUG:
            print data
        else:
            LOG.info(data)
    except:
        LOG.info(str(args))


def TRACE_ERROR(e):
    import traceback
    TRACE('str(Exception):\t%s', str(Exception))
    TRACE('str(e):\t\t%s', str(e))
    TRACE('repr(e):\t%s', repr(e))
    TRACE('e.message:\t%s', e.message)
    TRACE('traceback.print_exc():%s', traceback.print_exc())
    TRACE('traceback.format_exc():\n%s' % traceback.format_exc())


#pip install Pillow
#pip install inapppy==0.6
#pip install DBUtils
#pip install sqlalchemy