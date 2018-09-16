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
def TRACE(*args):
    if DEBUG:
        print str(''.join([str(a) for a in args])).encode('gbk').decode('gbk')
