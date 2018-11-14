# coding=utf-8
import os

from bottle import route, template, get, post, request, TEMPLATE_PATH, HTTPResponse, redirect
from common.captcha import create_validate_code
from common.core import *
from server_conf import BASE_DIR
TEMPLATE_PATH.append(os.path.join(BASE_DIR, 'views'))
from bottle import static_file

def UPDATE_COIN_USR_MONGY(db,uid,chips,reason):
    r=db.sql_dict("select CHIPS from coin_usr where ID=%d;",uid)
    before_chips=r['CHIPS']
    after_chips=before_chips+chips
    if after_chips<0:return False
    db.sql_exec("""
    INSERT INTO poker.coin_usr_chips_log( CID, BEFORE_CHIPS, AFTER_CHIPS, CHANGE_CHIPS, REASON) 
    VALUES (%d, %d, %d, %d, '%s');""",uid,before_chips,after_chips,chips,reason)
    return True

def coin_login_require(func):
    # 定义包装函数
    def wrapper(*args, **kargs):
        p = ParamWarper(request)
        if not p.session_uid:
            return redirect('/blg/console_login/')
        return func(*args, **kargs)
    return wrapper



@get('/coin/console_login/')
def coin_console_login():
    p=ParamWarper(request)
    def do_login():
        username, password, code = p.__username, p.__password, p.__code
        if str(code).lower() != str(p.session.get('code')).lower():
            return Fail("验证码错误")
        with DB() as db:
            r = db.sql_dict("select id from coin_usr where manager='%s' and password='%s'", username, password)
            if not r: return Fail("用户名或密码错误")
        p.session['uid'] = r['id']
    if p.__do_login:
        return do_login()
    return template("coin_login.html")


@get('/coin/console_main/')
def coin_console_main():
    p=ParamWarper(request)
    if not p.session.get('uid'):return redirect('/coin/console_login/')
    return template("main.html")





# users
@coin_login_require
@route('/coin/player_list/', method=['GET', 'POST'])
def coin_player_list():
    """玩家列表"""
    p = ParamWarper(request)
    if not p.session_uid:return Fail("登陆超时，请重新登陆")
    def add_chips():
        with DB() as db:
            chips=p.__chips
            receiverid=p.__uid
            if not UPDATE_COIN_USR_MONGY(db, p.session_uid,-chips,"赠送筹码"):
                return Fail("币商筹码余额不足")
            db.sql_exec("""
              INSERT INTO
                 poker.mail(
                   sendername
                  ,senderid
                  ,receiverid
                  ,title
                  ,content
                  ,sendtim
                  ,attachmenttype
                  ,attachmentnum
                  ,isread
                  ,mailtype
                  ,isgetattachment)
              VALUES
                 (
                      'System Mail'
                      ,1000
                      ,%d
                      ,'%s'
                      ,'%s'
                      ,now()
                      ,%d
                      ,%d
                      ,0
                      ,9
                      ,0
                  );
            """,receiverid, "筹码交易", "筹码交易，后台发放筹码，请注意查收。", 1, chips)
            db.commit()
        return SUCCESS

    if p.__add_chips:return add_chips()
    with DB() as db:
        condition = []
        if p.__UserID:
            condition.append(' `usr`.`usrid`=' + str(p.__UserID))
        if p.__UserName:
            condition.append("`usr`.`phone` LIKE ''%%" + p.trim__UserName + "%%''")
        if p.__NickName:
            condition.append("`usr`.`nickname` LIKE ''%%" + p.trim__NickName + "%%''")
        if p.__RegChannel:
            condition.append(' i.RegChannel=' + str(p.trim__RegChannel))
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName="`poker`.`usr`",
            columNames="""
                `usr`.`usrid` pk,
                `usr`.`nickname`,
                `usr`.`level`,
                `usr`.`moneyconsume`,
                `usr`.`lotto`,
                `usr`.`version`,
                `usr`.`chips`,
                `usr`.`regip`,
                `usr`.`regtime`,
                `usr`.`regdevice`,
                `usr`.`regversion`,
                `usr`.`versionid`,
                `usr`.`lastLogintm`,
                `usr`.`ai`,
                `usr`.`phone`,
                `usr`.`luck`,
                `usr`.`exp`,
                `usr`.`chipslimit`,
                `usr`.`disable`,
                `usr`.`level`
            """,
            orderBy='`usr`.`usrid` DESC',
            condition=' AND '.join(condition)
        )


@coin_login_require
@route('/coin/trade_log/', method=['GET', 'POST'])
def coin_trade_log():
    """交易日志"""
    p=ParamWarper(request)
    condition=[]
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName=" coin_usr_trade_log ",
            columNames="*",
            orderBy='ID DESC',
            condition=' AND '.join(condition)
        )


@coin_login_require
@route('/coin/chips_change_log/', method=['GET', 'POST'])
def coin_chips_change_log():
    """筹码变动日志"""
    p = ParamWarper(request)
    condition = []
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName=" coin_usr_trade_log ",
            columNames="*",
            orderBy='ID DESC',
            condition=' AND '.join(condition)
        )
