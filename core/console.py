# coding=utf-8
import os

from bottle import route, template, get, post, request, TEMPLATE_PATH, HTTPResponse, redirect
from common.captcha import create_validate_code
from common.core import *
from server_conf import BASE_DIR

TEMPLATE_PATH.append(os.path.join(BASE_DIR, 'views'))

from bottle import static_file


##########################################################

@get('/')
def index():
    return "HELLO WORLD"


def login_require(func):
    # 定义包装函数
    def wrapper(*args, **kargs):
        p = ParamWarper(request)
        if not p.session_uid:
            return redirect('/blg/console_login/')
        return func(*args, **kargs)

    return wrapper

def login_require_ajax(func):
    # 定义包装函数
    def wrapper(*args, **kargs):
        p = ParamWarper(request)
        if not p.session_uid:
            return Fail("用户登陆超时，请重新登陆",SESSSION_TIME_OUT=1)
        return func(*args, **kargs)
    return wrapper


##########################################################
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.path.join(BASE_DIR, 'static'))


@route('/blg/console_captcha/')
def console_captcha():
    import StringIO
    p = ParamWarper(request)
    mstream = StringIO.StringIO()
    img, code = create_validate_code()
    p.session['code'] = code
    img.save(mstream, "GIF")

    # p.request.session['code'] = code
    return HTTPResponse(body=mstream.getvalue(), content_type="image/gif")


@get('/blg/console_login/')
def console_login():
    return template("login.html")


@get('/blg/ad/')
def ad():
    return template("ad.html")


@post('/blg/console_login/')
def do_console_login():
    p = ParamWarper(request)
    username, password, code = p.__username, p.__password, p.__code
    if str(code).lower() != str(p.session.get('code')).lower():
        return Fail("验证码错误")

    with DB() as db:
        r = db.sql_dict("select id from gm_admin where manager='%s' and password='%s'", username, password)
        if not r: return Fail("用户名或密码错误")
    p.session['uid'] = r['id']
    return SUCCESS


@get('/blg/console_login_out/')
def do_login_out():
    p = ParamWarper(request)
    p.session.clear()
    return redirect('/blg/console_login/')


@login_require
@get('/blg/console_main/')
def console_main():
    p=ParamWarper(request)
    if not p.session.get('uid'):return redirect('/blg/console_login/')
    return template("main.html")


#######################################################
@get('/blg/user_info/')
@login_require_ajax
def user_info():
    p = ParamWarper(request)
    with DB() as db:
        ctx = db.sql_dict("""
            SELECT `usr`.`usrid`,
                    `usr`.`nickname`,
                    `usr`.`headicon`,
                    `usr`.`imheadurl`,
                    `usr`.`level`,
                    `usr`.`curtitle`,
                    `usr`.`exp`,
                    `usr`.`moneyconsume`,
                    `usr`.`banker`,
                    `usr`.`lotto`,
                    `usr`.`lottotimes`,
                    `usr`.`lottostock`,
                    `usr`.`chips`,
                    `usr`.`freechipcount`,
                    `usr`.`freechipstarttime`,
                    `usr`.`viprewardtime`,
                    `usr`.`savingpotchips`,
                    `usr`.`savingpotlevel`,
                    `usr`.`savintpotfullpush`,
                    `usr`.`payflag`,
                    `usr`.`firstpayflag`,
                    `usr`.`bigpayflag`,
                    `usr`.`vipchipflag`,
                    `usr`.`sevendayflag`,
                    `usr`.`openid`,
                    `usr`.`token`,
                    `usr`.`devicetoken`,
                    `usr`.`passporttype`,
                    `usr`.`regip`,
                    `usr`.`regtime`,
                    `usr`.`regdevice`,
                    `usr`.`regversion`,
                    `usr`.`versionid`,
                    `usr`.`ai`,
                    `usr`.`disable`,
                    `usr`.`phone`,
                    `usr`.`pwd`,
                    `usr`.`luck`,
                    lastLogintm
                FROM `poker`.`usr`
                WHERE usrid=%d;
        """, p.int__uid)
    return template("user_html_view.html", **ctx)


# users

@route('/blg/user_list/', method=['GET', 'POST'])
@login_require_ajax
def user_list():
    p = ParamWarper(request)
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
                `usr`.`chipslow`,
                `usr`.`disable`,
                `usr`.`level`,
                `usr`.`test`
            """,
            orderBy='`usr`.`usrid` DESC',
            condition=' AND '.join(condition)
        )



@post('/blg/do_edit_user_info/')
@login_require_ajax
def do_edit_user_info():
    p = ParamWarper(request)
    with DB() as db:
        if p.__update_luck:
            db.sql_exec("update usr  set luck=%d where usrid=%d;",p.int__luck,p.int__pk)
        else:
            db.sql_exec("""
                update usr 
                set chips=%d,lotto=%d,luck=%d,level=%d,exp=%d ,versionid='%s',disable=%d ,moneyconsume=%d,nickname='%s',test=%d
                where usrid=%d
            """, p.int__chips,
                        p.int__lotto,
                        p.int__luck,
                        p.int__level,
                        p.int__exp, p.__versionid, p.int__disable,p.__moneyconsume,p.__nickname, p.__test, p.int__pk)
        db.commit()
    return SUCCESS



@post('/blg/do_del_user_info/')
@login_require_ajax
def do_del_user_info():
    p = ParamWarper(request)
    pk = p.int__pk
    with DB() as db:
        r=db.sql_dict("select versionid from usr where usrid=%d;",pk)
        versionid=r.get('versionid') if r else ''
        db.sql_exec('delete from usr where usrid=%d', pk)
        db.sql_exec('delete from pay where usrId=%d', pk)
        db.sql_exec("call sp_gm_count(0,0,'PAY')")
        if versionid:db.sql_exec("call sp_gm_count_channel(0,0,'PAY','%s')",versionid)
        db.commit()
    return SUCCESS



@post('/blg/do_send_user_email/')
@login_require_ajax
def do_send_user_email():
    p = ParamWarper(request)
    email_title, email_money, email_content = \
        p.__email_title, p.__email_money, p.__email_content
    attach_type = 1 if email_money > 0 else 0
    with DB() as db:
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
                      ,0  
                      ,0  
                  );
        """, p.int__pk, email_title, email_content, attach_type, email_money)
        db.commit()
    return SUCCESS



@route('/blg/user_suggest_list/', method=['GET', 'POST'])
@login_require_ajax
def user_suggest_list():
    p = ParamWarper(request)
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName="`poker`.`feedback`",
            columNames="""
                    `feedback`.`id`,
                    `feedback`.`userid`,
                    `feedback`.`question`,
                    `feedback`.`reply`,
                    `feedback`.`questime`,
                    `feedback`.`type`,
                    `feedback`.`hander`,
                    `feedback`.`notify`
                """,
            orderBy='`feedback`.`id` DESC '
        )



@post('/blg/do_reply_user_suggest/')
@login_require_ajax
def do_reply_user_suggest():
    p = ParamWarper(request)
    reply_id, question = p.int__id, p.__question
    if not question: return Fail("回复内容不能为空")
    with DB() as db:
        db.sql_exec("""update feedback set reply='%s',`type`='已回复' where id=%d""", question, reply_id)
        db.commit()
    return SUCCESS


#######################################################
# 兑换

def exchange_approve_list():
    p = ParamWarper(request)
    with DB() as db:
        db.sql_padding(
            p.int__start,
            p.int__limit,
            tbName="""
                 exchange_approve_list l
                 LEFT JOIN exchange_config c ON l.EX_ID = c.ID
                 LEFT JOIN usr u ON l.UID = u.usrid
            """,
            columNames="""
                   l.ID,
                   l.CREATE_TIME,
                   l.EX_ID,
                   l.STATUS,
                   l.IS_APPROVE,
                   l.APPRIVE_TIME,
                   l.UID,
                   u.phone,
                   u.nickname
            """
        )


@route('/blg/exchange_config_list/', method=['GET', 'POST'])
@login_require_ajax
def exchange_config_list():
    with DB() as db:
        return db.sql_no_padding("""
            SELECT
            ID pk,ID
            ,NAME
            ,`POINT`
            ,STOCK
            ,CHIPS
            ,RTYPE
            ,GET_RATE
            ,GET_POINT
            ,LUCK_TYPE
            ,IS_PUSH
            FROM
             poker.exchange_config;
        """)



@post('/blg/exchange_config_list_add/')
@login_require_ajax
def exchange_config_list_add():
    p = ParamWarper(request)
    with DB() as db:
        db.sql_exec("""
            INSERT INTO
             exchange_config(
               NAME
              ,`POINT`
              ,STOCK
              ,CHIPS
              ,RTYPE
              ,GET_RATE
              ,GET_POINT
              ,LUCK_TYPE
              ,IS_PUSH)
            VALUES
             (
               '%s' -- NAME - IN varchar(255)
              ,%d -- POINT - IN int(11)
              ,%d -- STOCK - IN int(11)
              ,%d -- CHIPS - IN int(11)
              ,%d -- RTYPE - IN int(11)
              ,%d -- GET_RATE - IN float(11,0)
              ,%d -- GET_POINT - IN int(11)
              ,%d -- LUCK_TYPE - IN int(11)
              ,%d
                )
        """, p.__NAME
                    , p.__POINT
                    , p.__STOCK
                    , p.__CHIPS
                    , p.__RTYPE
                    , p.__GET_RATE
                    , p.__GET_POINT
                    , p.__LUCK_TYPE
                    , p.int__IS_PUSH)
        db.commit()
    return SUCCESS



@post('/blg/exchange_config_list_edit/')
@login_require_ajax
def exchange_config_list_edit():
    p = ParamWarper(request)
    with DB() as db:
        db.sql_exec("""
            UPDATE poker.exchange_config
            SET
               NAME = '%s' -- varchar(255)
              ,`POINT` = %d -- int(11)
              ,STOCK = %d -- int(11)
              ,CHIPS = %d -- int(11)
              ,RTYPE = %d -- int(11)
              ,GET_RATE = %d -- float(11,0)
              ,GET_POINT = %d -- int(11)
              ,LUCK_TYPE = %d -- int(11)
              ,IS_PUSH=%d
            WHERE ID = %d -- int(11)
        """, p.__NAME
                    , p.__POINT
                    , p.__STOCK
                    , p.__CHIPS
                    , p.__RTYPE
                    , p.__GET_RATE
                    , p.__GET_POINT
                    , p.__LUCK_TYPE, p.int__IS_PUSH,
                    p.int__ID)
        db.commit()
    return SUCCESS



@post('/blg/exchange_config_list_del/')
@login_require_ajax
def exchange_config_list_del():
    p = ParamWarper(request)
    with DB() as db:
        db.sql_exec("DELETE FROM poker.exchange_config WHERE ID = %d;", p.__pk)
        db.commit()
    return SUCCESS


# 兑换审核

@route('/blg/exchange_approve_list/', method=['GET', 'POST'])
@login_require_ajax
def exchange_approve_list():
    """兑换审核列表"""
    p = ParamWarper(request)
    with DB() as db:
        return db.sql_padding(
            p.int__start,
            p.int__limit,
            tbName="""
                 exchange_approve_list a
                 LEFT JOIN usr u ON a.UID = u.usrid
                 LEFT JOIN exchange_config e ON a.EX_ID = e.ID
            """,
            columNames="""
                 a.ID
                ,a.CREATE_TIME
                ,a.LXR
                ,a.ADDR
                ,a.PHONE
                ,a.EX_WAY
                ,e.NAME
                ,e.`POINT`
                ,u.usrid
                ,u.nickname
                ,u.moneyconsume
                ,u.lotto
                ,u.phone
            """,
            orderBy="a.ID DESC",
            condition="a.IS_APPROVE = 0"
        )



@post('/blg/do_exchange_approve/')
@login_require_ajax
def do_exchange_approve():
    """兑换审核"""
    p = ParamWarper(request)
    ID = p.int__ID
    IS_PASS = p.int__IS_PASS
    APPROVE_REMARK = p.__APPROVE_REMARK
    with DB() as db:
        db.sql_proc("sp_approve_ex_req", ID, IS_PASS, APPROVE_REMARK)
        db.commit()
    return SUCCESS



@route('/blg/exchange_approve_log_list/', method=['GET', 'POST'])
@login_require_ajax
def exchange_approve_log_list():
    """兑换审核日志"""
    p = ParamWarper(request)
    with DB() as db:
        return db.sql_padding(
            p.int__start,
            p.int__limit,
            tbName="""
                 exchange_log l
                 LEFT JOIN exchange_approve_list a ON l.APPROVE_ID = a.ID
                 LEFT JOIN exchange_config c ON l.EXID = c.ID
                 LEFT JOIN usr u ON l.UID = u.usrid
            """,
            columNames="""
                 l.ID
                ,c.POINT
                ,c.NAME
                ,c.RTYPE
                ,c.LUCK_TYPE
                ,l.UID
                ,l.EXTIME
                ,l.EXTYPE
                ,u.usrid
                ,u.nickname
                ,u.phone
                ,a.STATUS
                ,a.APPROVE_TIME
                ,a.LXR
                ,a.ADDR
                ,a.PHONE
                ,a.EX_WAY
                ,a.APPROVE_REMARK
            """,
            orderBy="l.ID DESC",
            condition=""
        )


#######################################################
# 版本控制
@route('/blg/channel_list/', method=['GET', 'POST'])
@login_require_ajax
def channel_list():
    with DB() as db:
        return db.sql_no_padding("""
            SELECT
             ID pk
            ,ID
            ,NAME
            ,NO
            ,remark
            ,platform
            ,app_id
            ,push_key
            ,push_mestersecret
            FROM
             channel
        """)



@post('/blg/do_edit_channel/')
@login_require_ajax
def do_edit_channel():
    p = ParamWarper(request)
    with DB() as db:
        db.sql_exec("""
            UPDATE
             poker.channel
            SET
             NAME              = '%s'
            ,NO                = '%s'
            ,remark            = '%s'
            ,platform          = '%s'
            ,app_id            = '%s'
            ,push_key          = '%s'
            ,push_mestersecret = '%s'
            WHERE ID=%d;
        """, p.__NAME, p.__NO, p.__remark, p.__platform, p.__app_id,
                    p.__push_key, p.__push_mestersecret, p.int__pk)
        db.commit()
    return SUCCESS



@route('/blg/version_list/', method=['GET', 'POST'])
@login_require_ajax
def version_list():
    with DB() as db:
        return db.sql_no_padding("""
            SELECT
             v.ID pk
            ,c.ID CID
            ,c.NAME
            ,c.NO
            ,v.NAME VNAME
            ,v.IS_APPROVE
            ,c.remark
            ,v.LAN_ID
            ,v.UPDATE_LINK
            ,v.USR_COUNT
            ,v.UPDATE_COUNT
            ,v.OPEN_MY_CARD_PAY
            FROM
             channel_version v LEFT JOIN channel c 
            ON v.CHANNEL_ID = c.ID
        """)




@post('/blg/do_add_version/')
@login_require_ajax
def do_add_version():
    p = ParamWarper(request)
    with DB() as db:
        db.sql_exec("""
                INSERT INTO poker.channel_version
                (NAME, IS_APPROVE, CHANNEL_ID, LAN_ID) 
                VALUES ('%s', %d, %d, %d);
        """, p.str__name, p.int__is_approve, p.int__channel_id, p.int__lan_id)
        db.commit()
    return SUCCESS



@post('/blg/do_edit_version/')
@login_require_ajax
def do_edit_version():
    p = ParamWarper(request)
    with DB() as db:
        db.sql_exec("""
                UPDATE poker.channel_version 
        SET NAME = '%s' , IS_APPROVE = %d, CHANNEL_ID = %d, LAN_ID = %d ,UPDATE_LINK='%s', OPEN_MY_CARD_PAY=%d
        WHERE id=%d-- Please complete
        ; """, p.str__VNAME, 1 if p.__IS_APPROVE in ('true',1) else 0, p.int__CID, p.int__LAN_ID, p.__UPDATE_LINK,
                    p.__OPEN_MY_CARD_PAY, p.__pk)
        db.commit()
    return SUCCESS



@post('/blg/do_del_version/')
@login_require_ajax
def do_del_version():
    p = ParamWarper(request)
    with DB() as db:
        db.sql_exec("""
        DELETE FROM poker.channel_version  WHERE ID = %d """, p.__pk)
        db.commit()
    return SUCCESS


#######################################################
# 跑马灯


@route('/blg/race_lamp_list/', method=['GET', 'POST'])
@login_require_ajax
def race_lamp_list():
    with DB() as db:
        return db.sql_no_padding("""
            SELECT id pk, gm_notice.* FROM gm_notice
        """)



@post('/blg/do_add_race_lamp/')
@login_require_ajax
def do_add_race_lamp():
    p = ParamWarper(request)
    with DB() as db:
        db.sql_exec("""
            INSERT INTO poker.gm_notice(
               repeatcount
              ,repeatgap
              ,content
              ,noticetime
              ,handler
              ,en_content
              ,channel
            ) VALUES (
               %d -- repeatcount - IN int(11)
              ,%d -- repeatgap - IN int(11)
              ,'%s' -- content - IN varchar(256)
              ,now()  -- noticetime - IN timestamp
              ,'admin' -- handler - IN varchar(255)
              ,'%s'
              ,'%s'
            )
        """, p.__repeatcount, p.__repeatgap, p.__content, p.__en_content,p.__channel)
        db.commit()
    return SUCCESS



@post('/blg/do_del_race_lamp/')
@login_require_ajax
def do_del_race_lamp():
    p = ParamWarper(request)
    with DB() as db:
        db.sql_exec("""
            delete from poker.gm_notice where id=%d
        """, p.int__pk)
        db.commit()
    return SUCCESS


#######################################################
# 订单

@route('/blg/pay_order_list/', method=['GET', 'POST'])
@login_require_ajax
def pay_order_list():
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
    c.append("p.paychannelname!=''COIN''")
    condition = ' AND '.join(c)
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName="""
                pay p INNER JOIN usr u ON p.usrId = u.usrid
            """,
            columNames="""
                 p.id
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

@route('/blg/pay_coin_order_list/', method=['GET', 'POST'])
@login_require_ajax
def pay_coin_order_list():
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
    c.append("p.paychannelname=''COIN''")
    condition = ' AND '.join(c)
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName="""
                pay p INNER JOIN usr u ON p.usrId = u.usrid
            """,
            columNames="""
                 p.id
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

#######################################################
@route('/blg/combo_channel/', method=['GET', 'POST'])
@login_require_ajax
def combo_channel():
    with DB() as db:
        return db.sql_combo("select ID pk,NAME name from channel")


#######################################################
# 游戏统计

def _cmp_game_count(rs):
    for r in rs['items']:
        # 两日留存
        r['D2_LEAVE_RATE_V'] = 0
        if r['YESTODAY_REG']:
            r['D2_LEAVE_RATE'] = str(round(r['DAY2_LEAVE'] * 1.0 / (r['YESTODAY_REG']), 3) * 100) + "%"
            r['D2_LEAVE_RATE_V'] = round(r['DAY2_LEAVE'] * 1.0 / (r['YESTODAY_REG']), 3) * 100
        else:
            r['D2_LEAVE_RATE'] = "0%"

        # 付费率
        r['PAY_RATE_V'] = 0
        if r['LOGIN_COUNT']:
            r['PAY_RATE'] = str(round(r['PAY_COUNT'] * 1.0 / r['LOGIN_COUNT'], 3) * 100) + '%'
            r['PAY_RATE_V'] = round(r['PAY_COUNT'] * 1.0 / r['LOGIN_COUNT'], 3) * 100
        else:
            r['PAY_RATE'] = "0%"

        # Arpu
        if r['LOGIN_COUNT']:
            r['ARPU'] = round(r['TOTAL_PAY'] * 1.0 / r['LOGIN_COUNT'], 3)
        else:
            r['ARPU'] = 0

        # Arppu
        if r['PAY_COUNT']:
            r['ARPPU'] = str(round(r['TOTAL_PAY'] * 1.0 / r['PAY_COUNT'], 3))
        else:
            r['ARPPU'] = 0



@route('/blg/game_count_list/', method=['GET', 'POST'])
@login_require_ajax
def game_count_list():
    p = ParamWarper(request)
    c = []
    ORDER = "DESC"
    if not p.__chart:
        start, limit = p.int__start, p.int__limit
    else:
        ORDER = "ASC"
        start, limit = 0, 20
        c.append('LOG_TIME>f_day(-20)')
    if p.__start_time:
        c.append("LOG_TIME > ''%s''" % p.__start_time)
    if p.__end_time:
        c.append("LOG_TIME < ''%s''" % p.__end_time)

    with DB() as db:
        rs = db.sql_padding(
            start=start,
            limit=limit,
            tbName="""gm_count""",
            columNames="""
                ID, 
                LOG_TIME, 
                LOGIN_COUNT LOGIN_COUNT, 
                REG_COUNT, 
                LOGIN_COUNT-REG_COUNT ACTVIE_COUNT,
                PAY_COUNT, 
                TOTAL_PAY, 
                DAY2_LEAVE,
                YESTODAY_LOGIN,
                YESTODAY_REG
            """,
            orderBy="ID " + ORDER,
            condition=' AND '.join(c)
        )
    _cmp_game_count(rs)
    return rs


@route('/blg/game_count_channel_list/', method=['GET', 'POST'])
@login_require_ajax
def game_count_channel_list():
    p = ParamWarper(request)
    c = []
    ORDER = "DESC"
    if not p.__chart:
        start, limit = p.int__start, p.int__limit
    else:
        ORDER = "ASC"
        start, limit = 0, 20
        c.append('LOG_TIME>f_day(-20)')
    if not p.__channel_id:
        c.append("CHANNEL = ''%s''" % "BLGOL")
    else:
        with DB() as db:
           r=db.sql_dict("select NO from channel where id=%d;",p.int__channel_id)
        c.append("CHANNEL = ''%s''" % r['NO'])
    if p.__start_time:
        c.append("LOG_TIME > ''%s''" % p.__start_time)
    if p.__end_time:
        c.append("LOG_TIME < ''%s''" % p.__end_time)
    with DB() as db:
        rs = db.sql_padding(
            start=start,
            limit=limit,
            tbName="""gm_count_channel""",
            columNames="""
                ID, 
                LOG_TIME, 
                LOGIN_COUNT LOGIN_COUNT, 
                REG_COUNT, 
                LOGIN_COUNT-REG_COUNT ACTVIE_COUNT,
                PAY_COUNT, 
                TOTAL_PAY, 
                DAY2_LEAVE,
                YESTODAY_LOGIN,
                YESTODAY_REG,
                CHANNEL
            """,
            orderBy="ID " + ORDER,
            condition=' AND '.join(c)
        )
    _cmp_game_count(rs)
    return rs


#######################################################
# 头像审核


@route('/blg/users_avastar_approve_list/', method=['GET', 'POST'])
@login_require_ajax
def users_avastar_approve_list():
    p = ParamWarper(request)
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName="avastar_approve",
            columNames="ID pk,  IMAGE_URL, UPLOAD_TIME,UID",
            orderBy="ID DESC"
        )



@post('/blg/do_users_avastar_approve/')
@login_require_ajax
def do_users_avastar_approve():
    p = ParamWarper(request)
    ids = p.ids__ids
    ids.append(0)
    is_pass = p.__is_pass == 1
    with DB() as db:
        if is_pass:
            db.sql_exec("""
                update usr u left join avastar_approve a on u.usrid=a.UID set u.imheadurl=CONCAT(a.IMAGE_URL,'!avastar') where a.ID in (%s)
            """, ','.join([str(a) for a in ids]))
        # 删除审核记录
        db.sql_exec("DELETE from avastar_approve where id in(%s)", ','.join([str(a) for a in ids]))
        db.commit()
    return SUCCESS


#######################################################


@route('/blg/game_win_count_list/', method=['GET', 'POST'])
@login_require_ajax
def game_win_count_list():
    p = ParamWarper(request)
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName="gm_win_count",
            columNames="*",
            orderBy="ID DESC"
        )


@route('/blg/user_money_log_list/', method=['GET', 'POST'])
@login_require_ajax
def user_money_log_list():
    p = ParamWarper(request)
    condition = []
    if p.__UID: condition.append(" UID = " + str(p.__UID))
    if p.__REASON: condition.append(" REASON like ''%%%s%%''" % p.__REASON)
    with DB() as db:
        return db.sql_padding_2(
            start=p.int__start,
            limit=p.int__limit,
            tbName="player_money_log p left join usr u on p.UID=u.usrid",
            autopk='p.id',
            columNames="p.*,u.nickname,u.phone,id pk",
            orderBy="ID DESC",
            condition=' AND '.join(condition)
        )


@route('/blg/user_lotto_log_list/', method=['GET', 'POST'])
@login_require_ajax
def user_lotto_log_list():
    p = ParamWarper(request)
    condition = []
    if p.__UID: condition.append(" UID = " + str(p.__UID))
    if p.__REASON: condition.append(" REASON like ''%%%s%%''" % p.__REASON)
    with DB() as db:
        return db.sql_padding_2(
            start=p.int__start,
            limit=p.int__limit,
            tbName="player_lotto_log p left join usr u on p.UID=u.usrid",
            autopk='p.id',
            columNames="p.*,u.nickname,u.phone,id pk",
            orderBy="ID DESC",
            condition=' AND '.join(condition)
        )


@route('/blg/user_ranking_log_list/', method=['GET', 'POST'])
@login_require_ajax
def user_ranking_log_list():
    p = ParamWarper(request)
    with DB() as db:
        rs= db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName="ranking3_log p left join usr u on p.UID=u.usrid",
            columNames="p.*,u.*",
            orderBy=" DT DESC,RANK ASC",
        )
    idx=0
    for r in rs['items']:
        r['items']['pk']=idx
        idx+=1
    return rs
#######################################################

@route('/blg/game_chips_count_list/', method=['GET', 'POST'])
@login_require_ajax
def game_chips_count_list():
    p = ParamWarper(request)
    if not p.__chart:
        start, limit = p.int__start, p.int__limit
    else:
        start, limit = 0, 90

    c = []
    if p.__start_time:
        c.append("LOG_TIME > ''%s''" % p.__start_time)
    if p.__end_time:
        c.append("LOG_TIME < ''%s''" % p.__end_time)

    with DB() as db:
        return db.sql_padding(
            start=start,
            limit=limit,
            tbName="gm_chips_count",
            columNames="*",
            orderBy="ID",
            condition=' AND '.join(c)
        )



@route('/blg/game_play_info/', method=['GET', 'POST'])
@login_require_ajax
def game_play_info():
    p = ParamWarper(request)
    condition = []
    if p.__UserID:
        condition.append(' `usr`.`usrid`=' + str(p.__UserID))
    if p.__UserName:
        condition.append("`usr`.`phone` LIKE ''%%" + p.trim__UserName + "%%''")
    if p.__NickName:
        condition.append("`usr`.`nickname` LIKE ''%%" + p.trim__NickName + "%%''")
    if p.__Channel:
        condition.append("`c`.`ID`=" + str(p.int__Channel))
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName="poker.playinfo p inner JOIN usr ON p.usrid = usr.usrid and usr.ai=0 left join channel c on usr.versionid=c.NO",
            columNames="""
                `usr`.`usrid` pk
                ,`usr`.`nickname`
                ,`usr`.`level`
                ,`usr`.`moneyconsume`
                ,`usr`.`lotto`
                ,`usr`.`chips`
                ,`usr`.`regip`
                ,`usr`.`regtime`
                ,`usr`.`regdevice`
                ,`usr`.`regversion`
                ,`usr`.`versionid`
                ,`usr`.`lastLogintm`
                ,`usr`.`phone`
                ,`usr`.`luck`
                ,`usr`.`exp`
                ,`usr`.`level`
                ,c.NAME CNAME
                ,p.*
            """,
            orderBy="usrid DESC",
            condition=' AND '.join(condition)
        )



@route('/blg/gm_send_chips_count/', method=['GET', 'POST'])
@login_require_ajax
def gm_send_chips_count():
    p = ParamWarper(request)
    condition = []
    if p.__chart:
        start, limit = 0, 90
        condition.append("REASON= ''筹码总发放''")
        orderBy = "TIM "
    else:
        start, limit = p.int__start, p.int__limit
        orderBy = "TIM DESC,COUNTS ASC"
    if p.__start_time:
        condition.append("TIM >= ''%s''" % p.__start_time)
    if p.__end_time:
        condition.append("TIM <= ''%s''" % p.__end_time)
    with DB() as db:
        return db.sql_padding(
            start=start,
            limit=limit,
            tbName="poker.gm_send_chips_count",
            columNames="""*""",
            orderBy=orderBy,
            condition=' AND '.join(condition)
        )



#######################################################

@route('/blg/coin_usr_list/', method=['GET', 'POST'])
@login_require_ajax
def blg_coin_usr_list():
    p=ParamWarper(request)

    def add_coin_usr():
        USRNAME,NICKNAME,CHIPS,PWD=p.__USRNAME,p.__NICKNAME,p.__CHIPS,p.__PWD
        with DB() as db:
            if db.sql_exists("select 1 from coin_usr where USRNAME='%s';",USRNAME):
                return Fail("用户名已存在")
            db.sql_exec("""
                INSERT INTO poker.coin_usr
                (USRNAME, CHIPS, PWD, NICKNAME, ENABLE) 
                VALUES ('%s', %d, '%s', '%s', 1);
            """,USRNAME,CHIPS,PWD,NICKNAME)
            db.commit()
            return SUCCESS

    def edit_coin_usr():
        ID, USRNAME, NICKNAME, CHIPS, PWD,ENABLE ,GAME_UID=\
            p.__ID, p.__USRNAME, p.__NICKNAME, p.__CHIPS, p.__PWD,p.__ENABLE,p.__GAME_UID
        with DB() as db:
            if db.sql_exists("select 1 from coin_usr where USRNAME='%s' AND ID!=%d;",USRNAME,ID):
                return Fail("用户名已存在")
            r = db.sql_dict("select CHIPS from coin_usr where ID=%d;", ID)
            before_chips = r['CHIPS']
            db.sql_exec("""
                UPDATE poker.coin_usr 
                SET USRNAME = '%s', CHIPS = %d, PWD = '%s', NICKNAME = '%s',ENABLE=%d,GAME_UID=%d
                WHERE ID=%d; """,USRNAME,CHIPS,PWD,NICKNAME,ENABLE,GAME_UID,ID)
            after_chips=CHIPS
            db.sql_exec("""
            INSERT INTO poker.coin_usr_chips_log( CID, BEFORE_CHIPS, AFTER_CHIPS, CHANGE_CHIPS, REASON) 
            VALUES (%d, %d, %d, %d, '%s');""", ID, before_chips, after_chips, after_chips-before_chips, "管理员修改")
            db.commit()
            return SUCCESS

    if p.__add:return add_coin_usr()
    if p.__edit:return edit_coin_usr()
    with DB() as db:
        return db.sql_no_padding("select ID pk, coin_usr.* from coin_usr")


############################################################################################



@route('/blg/coin_usr_chips_change_log/', method=['GET', 'POST'])
@login_require_ajax
def blg_coin_usr_chips_change_log():
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



@route('/blg/coin_usr_chips_trade_log/', method=['GET', 'POST'])
@login_require_ajax
def blg_coin_usr_chips_trade_log():
    p = ParamWarper(request)
    condition = []
    with DB() as db:
        return db.sql_padding(
            start=p.int__start,
            limit=p.int__limit,
            tbName="""
                         coin_usr_trade_log l
                         LEFT JOIN coin_usr c ON l.CID = c.ID
                         LEFT JOIN usr u ON l.UID = u.usrid
                    """,
            columNames="""
                         c.USRNAME CUSRNAME
                        ,c.ID
                        ,l.ID pk
                        ,c.CHIPS CCHIPS
                        ,c.NICKNAME CNICKNAME
                        ,l.CID
                        ,l.PRE_CHIPS
                        ,l.RMB
                        ,l.CHIPS
                        ,l.TM
                        ,u.usrid
                        ,u.nickname
                        ,u.curtitle
                        ,u.moneyconsume
                        ,u.chips
                    """,
            orderBy='l.ID DESC',
            condition=' AND '.join(condition)
        )




@route('/blg/coin_usr_chips_config/', method=['GET', 'POST'])
@login_require_ajax
def blg_coin_usr_chips_config():
    p = ParamWarper(request)

    def add_cfg():
        with DB() as db:
            db.sql_exec("""
                INSERT INTO poker.coin_usr_chips_config
                (CHIPS, RMB, NT) 
                VALUES (%d, %f, %f);
            """,p.__CHIPS,p.__RMB,p.__NT)
            db.commit()
            return SUCCESS

    def delete_cfg():
        with DB() as db:
            db.sql_exec("delete from coin_usr_chips_config where ID=%d;",p.__ID)
            db.commit()
        return SUCCESS

    def edit_cfg():
        with DB() as db:
            db.sql_exec("""
                UPDATE poker.coin_usr_chips_config 
                SET CHIPS = %d , RMB = %f, NT = %f 
                WHERE ID=%d;
            """,p.__CHIPS,p.__RMB,p.__NT,p.__ID)
            db.commit()
        return SUCCESS

    if p.__add:return add_cfg()
    if p.__edit:return edit_cfg()
    if p.__delete:return delete_cfg()

    with DB() as db:
        return db.sql_no_padding("select * from coin_usr_chips_config")
#######################################################

@route('/blg/game_watch/', method=['GET', 'POST'])
@login_require_ajax
def game_watch():
    p=ParamWarper(request)
    def edit():
        with DB() as db:
            db.sql_exec("update game_watch set RESTART_TIME='%s' where GAME_NAME='%s';"
                        ,p.__RESTART_TIME,p.__GAME_NAME)
            db.commit()
            return SUCCESS

    if p.__edit:return edit()
    with DB() as db:
        return db.sql_no_padding("select * from game_watch")

