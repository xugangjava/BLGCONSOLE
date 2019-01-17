# coding=utf-8
import os

from bottle import route, template, get, post, request, TEMPLATE_PATH, HTTPResponse, redirect
from common.captcha import create_validate_code
from common.core import *
from server_conf import BASE_DIR
TEMPLATE_PATH.append(os.path.join(BASE_DIR, 'views'))
from bottle import static_file

def UPDATE_COIN_USR_MONGY(db,cid,chips,reason,uid):
    r=db.sql_dict("select CHIPS,PARENT from coin_usr where ID=%d;",cid)
    parent=r['PARENT']
    if parent:
        #上级额度
        r = db.sql_dict("select CHIPS from coin_usr where ID=%d;", parent)
    before_chips=r['CHIPS']
    after_chips=before_chips+chips
    if after_chips<0:return False
    db.sql_exec("""
    INSERT INTO poker.coin_usr_chips_log( CID, BEFORE_CHIPS, AFTER_CHIPS, CHANGE_CHIPS, REASON,UID) 
    VALUES (%d, %d, %d, %d, '%s',%d);""",cid,before_chips,after_chips,chips,reason,uid)
    if parent:
        db.sql_exec("update coin_usr set CHIPS=CHIPS+%d where ID=%d;", chips, parent)
    else:
        db.sql_exec("update coin_usr set CHIPS=CHIPS+%d where ID=%d;",chips,cid)
    return True

def coin_login_require(func):
    # 定义包装函数
    def wrapper(*args, **kargs):
        p = ParamWarper(request)
        if not p.session_cuid:
            return redirect('/coin/console_login/')
        return func(*args, **kargs)
    return wrapper

def coin_login_require_ajax(func):
    # 定义包装函数
    def wrapper(*args, **kargs):
        p = ParamWarper(request)
        if not p.session_cuid:
            return Fail("用户登陆超时，请重新登陆",SESSSION_TIME_OUT=1)
        return func(*args, **kargs)
    return wrapper


@route('/coin/console_login/',method=['GET', 'POST'])
def coin_console_login():
    p=ParamWarper(request)
    def do_login():
        username, password, code = p.__username, p.__password, p.__code
        if str(code).lower() != str(p.session.get('code')).lower():
            return Fail("验证码错误")
        with DB() as db:
            r = db.sql_dict("select id from coin_usr where USRNAME='%s' and PWD='%s' and ENABLE=1;", username, password)
            if not r: return Fail("用户名或密码错误")
        p.session['cuid'] = r['id']
        return SUCCESS
    if p.__do_login:
        return do_login()
    return template("coin_login.html")


@route('/coin/console_main/', method=['GET', 'POST'])
@coin_login_require
def coin_console_main():
    p=ParamWarper(request)
    with DB() as db:
        r = db.sql_dict("select CHIPS,NICKNAME,PARENT from coin_usr where ID=%d;", p.session_cuid)
        if r['PARENT']:
            chips = db.sql_dict("select CHIPS from coin_usr where ID=%d;", p.session_cuid)['CHIPS']
        else:
            chips = r['CHIPS']
    return template("coin_main.html", chips=chips, nickname=r['NICKNAME'],parent=1 if r['PARENT'] else 0)



# users

@route('/coin/player_list/', method=['GET', 'POST'])
@coin_login_require_ajax
def coin_player_list():
    """玩家列表"""
    p = ParamWarper(request)
    def add_chips():
        with DB() as db:
            if int(p.__CHIPS)<0:
                return Fail("筹码必须为正整数")
            uid=p.__pk
            usr=db.sql_dict("select versionid,regdevice,version from usr where usrid=%d;",uid)
            payconfig=db.sql_dict("select CHIPS,RMB from coin_usr_chips_config where ID=%d;",p.__payid)
            usrId, payNum, payid,  ibeiId, payType, rmb, rmb, chips, version , platfrom, versionid, thirdpay, IAPID= \
                uid, guid(), 10000,  10000, 10000, int(payconfig['RMB']), int(payconfig['RMB']), p.__CHIPS, \
                usr['versionid'], usr['regdevice'], usr['version'], "COIN", str(p.__payid),
            payNum=guid()
            if not UPDATE_COIN_USR_MONGY(db, p.session_cuid,-chips,"售出筹码",usrId):
                return Fail("币商筹码余额不足")
            db.sql_exec("""
            INSERT INTO poker.pay
            (usrId, payNum, ibeiId, itemId, itemType, dollar, realdollar, chips, recommend, tim, verify, paychannel, 
            orderid, versionid, platfrom, versionname, paychannelname, iapid,cid) 
            VALUES 
            (%d, '%s', %d, %d, %d, %d, %d, %d, %d, now(), %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s',%d); """,
            usrId, payNum, ibeiId, 10000, 10000, rmb, rmb, chips, 0, 0,
            "COIN",
            "", versionid, platfrom, version, "COIN", IAPID,p.session_cuid)
            transaction_id,out_trade_no=payNum,payNum
            db.sql_exec("""
                 INSERT INTO poker.paycallback
                 (TRANID, PAYID) 
                 VALUES ('%s', '%s');
             """, transaction_id, out_trade_no)
            db.commit()
        return SUCCESS

    def chips_point_combo():
        with DB() as db:
            return db.sql_combo("select ID pk, NT name from coin_usr_chips_config ORDER  BY NT ASC;")

    if p.__add_chips:return add_chips()
    if p.__combo:return chips_point_combo()

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



@route('/coin/trade_log/', method=['GET', 'POST'])
@coin_login_require_ajax
def coin_trade_log():
    """交易日志"""
    p=ParamWarper(request)
    condition=[]
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName=" coin_usr_trade_log ",
            columNames="ID pk, coin_usr_trade_log.*",
            orderBy='ID ASC',
            condition=' AND '.join(condition)
        )


@route('/coin/chips_change_log/', method=['GET', 'POST'])
@coin_login_require_ajax
def coin_chips_change_log():
    """筹码变动日志"""
    p = ParamWarper(request)
    c = []
    if p.__uid:
        c.append("u.usrid=%d" % p.int__uid)
    if p.__name:
        c.append("u.nickname like ''%%%s%%''" % p.__name)
    if p.__nick:
        c.append("u.nickname like ''%%%s%%''" % p.__nick)
    if p.__start_time:
        c.append("l.DT > ''%s''" % p.__start_time)
    if p.__end_time:
        c.append("l.DT < ''%s''" % p.__end_time)
    c.append("(l.CID=%d or c.PARENT=%d)" % (p.session_cuid,p.session_cuid))
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName="""
                     coin_usr_chips_log l
                     LEFT JOIN coin_usr c ON l.CID = c.ID
                     LEFT JOIN usr u ON l.UID = u.usrid
                """,
            columNames="""
                     c.USRNAME CUSRNAME
                    ,l.ID pk
                    ,c.ID
                    ,c.CHIPS CCHIPS
                    ,c.NICKNAME CNICKNAME
                    ,l.CID
                    ,l.BEFORE_CHIPS
                    ,l.AFTER_CHIPS
                    ,l.CHANGE_CHIPS
                    ,l.REASON
                    ,l.DT
                    ,u.usrid
                    ,u.nickname
                    ,u.curtitle
                    ,u.moneyconsume
                    ,u.chips
                """,
            orderBy='l.ID DESC',
            condition=' AND '.join(c)
        )



@get('/coin/console_login_out/')
def coin_console_login_out():
    p = ParamWarper(request)
    p.session.clear()
    return redirect('/coin/console_login/')



# 订单

@route('/coin/pay_order_list/', method=['GET', 'POST'])
@coin_login_require
def coin_pay_order_list():
    p = ParamWarper(request)
    c = []
    if p.__uid:
        c.append("u.usrId=%d" % p.int__uid)
    if p.__name:
        c.append("u.nickname like ''%%%s%%''" % p.__name)
    if p.__nick:
        c.append("u.nickname like ''%%%s%%''" % p.__nick)
    if p.__start_time:
        c.append("p.tim > ''%s''" % p.__start_time)
    if p.__end_time:
        c.append("p.tim < ''%s''" % p.__end_time)
    if p.__nopay == 'true' or not p.__nopay:
        c.append('p.verify=1')
    c.append("(p.cid="+str(p.session_cuid) +" or c.PARENT="+str(p.session_cuid)+")")
    condition = ' AND '.join(c)
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName="""
                pay p INNER JOIN usr u ON p.usrId = u.usrid LEFT JOIN coin_usr c ON p.cid=c.ID
            """,
            columNames="""
                 p.id
                ,p.id pk
                ,p.usrId
                ,p.payNum
                ,p.ibeiId
                ,p.itemId
                ,p.itemType
                ,p.dollar
                ,p.realdollar
                ,p.chips
                ,p.recommend
                ,p.tim
                ,p.verify
                ,p.paychannel
                ,p.orderid
                ,p.versionid
                ,p.platfrom
                ,p.versionname
                ,p.paychannelname
                ,u.usrid
                ,u.nickname
                ,u.level
                ,u.moneyconsume
                ,u.regip
                ,u.regtime
                ,u.regdevice
                ,u.phone
                ,u.lastLogintm
            """,
            condition=condition,
            orderBy='  p.tim DESC '
        )




@route('/coin/race_lamp_list/', method=['GET', 'POST'])
@coin_login_require
def coin_race_lamp_list():
    p=ParamWarper(request)
    def add():
        with DB() as db:
            r=db.sql_dict("select GAME_UID from coin_usr where ID=%d;",p.session_cuid)
            db.sql_exec("""
                INSERT INTO poker.gm_coin_notice(
                   repeatcount
                  ,repeatgap
                  ,content
                  ,noticetime
                  ,handler
                  ,en_content
                  ,channel
                  ,uid
                ) VALUES (
                   %d -- repeatcount - IN int(11)
                  ,%d -- repeatgap - IN int(11)
                  ,'%s' -- content - IN varchar(256)
                  ,now()  -- noticetime - IN timestamp
                  ,'admin' -- handler - IN varchar(255)
                  ,'%s'
                  ,'%s'
                  ,%d
                )
            """, p.__repeatcount, p.__repeatgap, p.__content, p.__en_content, p.__channel,r['GAME_UID'])
            db.commit()
        return SUCCESS

    def delete():
        with DB() as db:
            db.sql_exec("""
                   delete from poker.gm_coin_notice where id=%d
               """, p.int__pk)
            db.commit()
        return SUCCESS

    if p.__add==1:return add()
    if p.__del==1:return delete()
    with DB() as db:
        r = db.sql_dict("select GAME_UID from coin_usr where ID=%d;", p.session_cuid)
        return db.sql_no_padding("""
            SELECT id pk, gm_coin_notice.* FROM gm_coin_notice WHERE uid=%d
        """,r['GAME_UID'])


@route('/coin/coin_usr_list/', method=['GET', 'POST'])
@coin_login_require_ajax
def coin_coin_usr_list():
    p=ParamWarper(request)
    with DB() as db:
        r=db.sql_dict("select PARENT from coin_usr where ID=%d;",p.session_cuid)
        if r['PARENT']:return Fail("只有0级分销商可以添加下层")

    def add_coin_usr():
        USRNAME,NICKNAME,PWD=p.__USRNAME,p.__NICKNAME,p.__PWD
        with DB() as db:
            if db.sql_exists("select 1 from coin_usr where USRNAME='%s';",USRNAME):
                return Fail("用户名已存在")
            db.sql_exec("""
                INSERT INTO poker.coin_usr
                (USRNAME, CHIPS, PWD, NICKNAME, ENABLE,PARENT) 
                VALUES ('%s', %d, '%s', '%s', 1,%d);
            """,USRNAME,0,PWD,NICKNAME,p.session_cuid)
            db.commit()
            return SUCCESS

    def edit_coin_usr():
        ID, USRNAME, NICKNAME,  PWD,ENABLE ,GAME_UID=\
            p.__ID, p.__USRNAME, p.__NICKNAME,  p.__PWD,p.__ENABLE,p.__GAME_UID
        with DB() as db:
            if db.sql_exists("select 1 from coin_usr where USRNAME='%s' AND ID!=%d;",USRNAME,ID):
                return Fail("用户名已存在")
            db.sql_exec("""
                UPDATE poker.coin_usr 
                SET USRNAME = '%s', PWD = '%s', NICKNAME = '%s',ENABLE=%d,GAME_UID=%d
                WHERE ID=%d AND PARENT=%d; """,USRNAME,PWD,NICKNAME,ENABLE,GAME_UID,ID,p.session_cuid)
            db.commit()
            return SUCCESS

    if p.__add:return add_coin_usr()
    if p.__edit:return edit_coin_usr()
    with DB() as db:
        return db.sql_no_padding("select ID pk, coin_usr.* from coin_usr WHERE  PARENT=%d;",p.session_cuid)

@route('/coin/query_chips_limit/', method=['GET', 'POST'])
@coin_login_require_ajax
def coin_query_chips_limit():
    p = ParamWarper(request)
    with DB() as db:
        r = db.sql_dict("select CHIPS,PARENT from coin_usr where ID=%d;", p.session_cuid)
        parent = r['PARENT']
        if parent:
            # 上级额度
            r = db.sql_dict("select CHIPS from coin_usr where ID=%d;", parent)
    return Success("",chips=r['CHIPS'])


@route('/coin/edit_password/', method=['GET', 'POST'])
@coin_login_require_ajax
def coin_edit_password():
    p = ParamWarper(request)
    curpwd,newpwd,cnewpwd=str(p.str__curpwd),str(p.str__newpwd),str(p.str__cnewpwd)
    if newpwd!=cnewpwd:
        return Fail("密码确认不一致")
    if len(newpwd)<6:
        return Fail("新密码长度必须大于等于6")
    with DB() as db:
        r=db.sql_dict("select PWD from coin_usr where ID=%d;",p.session_cuid)
        if r['PWD']!=curpwd:
            return Fail("旧密码输入错误，请联上级系管理员找回密码")
        db.sql_exec("update coin_usr set pwd='%s' where id=%d;",newpwd, p.session_cuid)
        db.commit()
    return SUCCESS

