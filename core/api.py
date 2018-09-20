# coding=utf-8
import sitecustomize
from bottle import post, request, error, HTTPResponse, get, view,route
from common.pay import *
from common.sms import *


#######################################################
# 验证码相关 绑定账号
def _send_code(phone, operator, code_type):
    """发送验证码"""
    code = int(random.randint(1000, 9999))
    if sms_code(code, phone, operator):
        with DB() as db:
            db.sql_proc("sp_send_phone_code",
                        phone,
                        code,
                        code_type)
            db.commit()
        return Success("验证码发送成功", CODE=code)
    else:
        return Fail("验证码发送失败请重试")


def _verify_code(db, phone, code, code_type):
    """校验验证码"""
    return db.sql_exists("""
        SELECT 1
        FROM phone_verify
        WHERE CODE = %d AND PHONE = '%s' AND CODE_TYPE = %d
    """, int(code), phone, code_type)


def _is_usr_bind_phone(db, uid):
    r = db.sql_dict("select phone from	usr where usrid='%d'", uid)
    return r['phone'] != ''


def _is_phone_exists(db, phone):
    if not phone: return 0
    r = db.sql_dict("select usrid from	usr where openid='%s'", phone)
    return 0 if not r else r['usrid']


#######################################################
# 注册
@post('/api/sms_register_sms_code/')
def api_sms_register_sms_code():
    """发送注册验证码"""
    p = ParamWarper(request)
    phone = p.__phone
    if not phone: return Fail("手机号不能为空")
    phone = str(phone)
    with DB() as db:
        if _is_phone_exists(db, phone):
            return Fail('该手机号已注册')
    return _send_code(phone, '账号注册', 1)


#######################################################
# 找回密码
@post('/api/sms_find_password/')
def api_sms_find_password():
    """找回密码验证码"""
    p = ParamWarper(request)
    phone = p.__phone
    if not phone: return Fail("手机号不能为空")
    phone = str(phone)
    with DB() as db:
        if not _is_phone_exists(db, str(phone)):
            return Fail('用户名不存在')
    return _send_code(phone, '找回密码', 2)


@post('/api/player_reset_password/')
def api_player_reset_password():
    """重置密码"""
    p = ParamWarper(request)
    phone = p.__phone
    if not phone: return Fail("手机号不能为空")
    phone = str(phone)
    if not p.__TOKEN: return Fail("新密码不能为空")
    with DB() as db:
        uid = _is_phone_exists(db, phone)
        if not uid:
            return Fail('账号不存在')

        if not _verify_code(db, phone, p.__code, 2):
            return Fail("验证码错误")

        db.sql_exec("update usr set  pwd='%s' where usrid=%d", p.__TOKEN, uid)
        db.commit()

    return SUCCESS


#######################################################
@post('/api/sms_bind_user/')
def api_sms_bind_user():
    """绑定账号"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    phone = p.__phone
    if not phone: return Fail("手机号不能为空")
    phone = str(phone)
    with DB() as db:
        if _is_phone_exists(db, phone):
            return Fail('该手机号已绑定')
        if _is_usr_bind_phone(db, p.uid):
            return Fail("该用户已绑定")
    return _send_code(phone, '绑定账号', 3)


@post('/api/player_is_bind/')
def api_player_is_bind():
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    with DB() as db:
        r = db.sql_dict("select phone from usr where usrid=%d", p.uid)
    return OK(BIND=r['phone'] != '' if r else False)


@post('/api/player_bind_account/')
def api_player_bind_account():
    """绑定账号"""
    p = ParamWarper(request)

    if not p.uid: return TOKEN_ERROR
    phone = p.__phone
    pwd = p.__pwd
    if not phone: return Fail("手机号不能为空")
    phone = str(phone)
    with DB() as db:
        if _is_phone_exists(db, phone):
            return Fail('该手机号已绑定')
        if _is_usr_bind_phone(db, p.uid):
            return Fail("该用户已绑定")
        if not _verify_code(db, phone, p.__code, 3):
            return Fail("验证码错误")

        db.sql_exec("update usr set  openid='%s',phone='%s',"
                    "passporttype='phone',pwd='%s' where usrid=%d",
                    phone,
                    phone,
                    pwd,
                    p.uid)
        db.commit()
    return SUCCESS


# #######################################################
# #头像上传
# @post('/api/avatar_upload_callback/')
# def api_avatar_upload_callback():
#     """创建订单"""
#     p = ParamWarper(request)
#     image_url=p.__image_url
#
#     return SUCCESS
#
#######################################################
# 支付
FISRT_PLAY_ID = 100002


def _check_first_pay():
    p = ParamWarper(request)
    p_payid = p.__p_payid  # 支付ID
    if p_payid == FISRT_PLAY_ID:
        with DB() as db:
            o = db.sql_o("select moneyconsume from usr where usrid=%d", p.uid)
        if o.moneyconsume > 0:
            return Fail(p.string(1009))
    return None


def _create_order(pay_way):
    """数据库创建订单"""

    p = ParamWarper(request)

    # if pay_way == 'wx':
    #     prefx = 'wx'
    # elif pay_way == 'alipay':
    #     prefx = 'ap'
    # else:
    #     prefx = 'ios'
    p_payway = pay_way  # 支付方式 wx alipay ios google

    p_payno = ''.join(str(uuid.uuid1()).split('-')).upper()
    p_payid = p.__p_payid  # 支付ID
    p_channel = p.__p_channel  # 支付渠道名称 BLGYLC
    p_orderid = ""
    p_version_id = p.__p_version_id  # 客户端版本号 1.0.1
    p_game_name = p.__p_game_name  # 客户端游戏名称 百乐宫娱乐城
    p_uid = p.uid
    total_fee = 0
    if not all([p_payid, p_channel, p_version_id, p_game_name]): return 0, 0
    with DB() as db:
        db.sql_proc("sp_create_pay_order",
                    p_payno,
                    p_payid,
                    p_channel,
                    p_orderid,
                    p_version_id,
                    p_payway,
                    p_game_name,
                    p_uid)
        db.commit()
    r = db.proc_result
    if r and r[0]['RESULT'] == 1:
        total_fee = r[0]['RMB'] * 100
    if PAY_DEBUG: total_fee = 1
    return total_fee, p_payno


# 支付
@post('/api/h5_alipay_create_order/')
def api_h5_alipay_create_order():
    """创建订单"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    r = _check_first_pay()
    if r: return r
    total_fee, p_payno = _create_order('alipay')
    if not total_fee or not p_payno: return Fail("创建订单失败")
    pay_url = AliPay.create_pay_url(
        out_trade_no=p_payno,
        total_amount=str(total_fee / 100.0),
        subject="真人百家乐购买筹码")
    return Success(
        oto=p_payno,
        py=pay_url
    )


@post('/api/h5_wx_create_order/')
def api_h5_wx_create_order():
    """创建微信订单"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    r = _check_first_pay()
    if r: return r
    total_fee, p_payno = _create_order('wx')
    if not total_fee or not p_payno: return Fail("创建订单失败")
    nonce_str = H5WXPlay.gen_nonce_str()
    spbill_create_ip = get_client_ip(request)
    TRACE("WX CLIENT IP:", spbill_create_ip)
    wxpay = H5WXPlay(
        out_trade_no=p_payno,
        body="真人百家乐购买筹码",
        total_fee=total_fee,
        nonce_str=nonce_str,
        spbill_create_ip=spbill_create_ip,
        trade_type='MWEB')
    params = wxpay.proceed()
    if not params:
        return Fail("创建订单失败")
    # 保存请求信息
    mweb_url = wxpay.mweb_url
    params['out_trade_no'] = p_payno
    mweb_url += '&redirect_url=http%3A%2F%2Fblgserver.billionocean.cn:8000/h5_wx_pay_redirect_url/'
    return Success(
        mweb_url='/h5_wx_pay_url/?mweb_url=' + base64.b64encode(mweb_url) + '&r=' + str(random.random()),
        oto=p_payno
    )


@get('/h5_wx_pay_url/')
@view('wx_pay_url.html')
def api_h5_wx_pay_url():
    p = ParamWarper(request)
    mweb_url = base64.b64decode(p.__mweb_url)
    return {"mweb_url": mweb_url, 'redirect': "FALSE"}


@get('/h5_wx_pay_redirect_url/')
@view('wx_pay_url.html')
def api_h5_wx_pay_redirect_url():
    return {"mweb_url": "", 'redirect': "TRUE"}


@post('/api/aplipay_notify_url/')
def api_aplipay_notify_url():
    """支付宝回调"""
    TRACE("ALIPAYNOTIFY:=======")
    data = dict(request.POST)
    success = AliPay.verify_notify(data)
    if success:
        out_trade_no = data['out_trade_no']
        trade_status = data["trade_status"]
        trade_no = data['trade_no']
        if trade_status == 'TRADE_SUCCESS':
            with DB() as db:
                db.sql_proc("sp_pay_notify", out_trade_no, trade_no)
                db.commit()
        return HTTPResponse("success", content_type="text/xml")
    return error(404)


@post('/api/wxpay_notify_url/')
def api_wxpay_notify_url():
    """微信回调"""
    wx = H5WXPlay()
    if not wx.verify_notify(request.body):
        return error(404)

    def to_xml(raw):
        s = ""
        for k, v in raw.items():
            s += "<{0}>{1}</{0}>".format(k, v)
        s = "<xml>{0}</xml>".format(s)
        return s.encode("utf-8")

    r = wx.notify_xml_string_to_dict(request.body)

    out_trade_no = r['out_trade_no']
    return_code = r['return_code']
    transaction_id = r['transaction_id']
    if return_code == 'SUCCESS':
        with DB() as db:
            db.sql_proc("sp_pay_notify", out_trade_no, transaction_id)
            db.commit()

    return HTTPResponse(
        to_xml(dict(return_code=r['return_code'], return_msg="OK")),
        content_type="text/xml")


########################################
# google支付

@post('/api/google_play_create_order/')
def api_google_play_create_order():
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    r = _check_first_pay()
    if r: return r
    total_fee, p_payno = _create_order('google')
    return Success(
        total_fee=total_fee,
        oto=p_payno
    )


# @post('/api/google_play_callback/')
# def api_google_play_callback():
#     p = ParamWarper(request)
#     out_trade_no = p.__out_trade_no
#     rt = p.__refresh_token
#     bill_id, package_name, product_id, purchase_token = p.__bill_id, p.__package_name, p.__product_id, p.__purchase_token
#     TRACE("PARAM:", bill_id, package_name, product_id, purchase_token)
#     checker = GooglePay(rt)
#     if checker.check_purchase(bill_id, package_name, product_id, purchase_token):
#         with DB() as db:
#             db.sql_proc("sp_pay_notify", out_trade_no, bill_id)
#             db.commit()
#     return OK()


# @post('/api/ios_pay_callback/')
# def api_ios_pay_callback():
#     """IOS回调"""
#     p = ParamWarper(request)
#     # if not p.uid: return TOKEN_ERROR
#     # out_trade_no = p.__out_trade_no
#     # with DB() as db:
#     #     db.sql_proc("sp_pay_notify", out_trade_no, out_trade_no)
#     #     db.commit()
#     # return SUCCESS
#     import httplib
#     # uid = p.uid
#     out_trade_no = p.__out_trade_no
#     # is_sand_box = p.__is_sand_box
#     game_no = p.__game_no
#     version = p.__version
#     params = request.POST.get('params', '')
#     if not params:
#         return Fail("参数错误")
#     pay_receipt_dict = json.loads(params)
#     pay_receipt_data = pay_receipt_dict.get('receipt-data')
#     pay_receipt = json.dumps({'receipt-data': pay_receipt_data})
#     headers = {"Content-type": "application/json"}
#     is_sand_box = 0
#     with DB() as db:
#         r = db.sql_dict(""" select v.IS_APPROVE from channel_version v
#                                        left join channel c on v.CHANNEL_ID=c.ID
#                                        where c.NO='%s' and v.NAME='%s'; """, game_no, version)
#
#     if r and r['IS_APPROVE'] == 0:
#         is_sand_box = 1
#
#     if is_sand_box:
#         # 测试地址
#         connect = httplib.HTTPSConnection("sandbox.itunes.apple.com")
#     else:
#         # 正式地址
#         connect = httplib.HTTPSConnection("buy.itunes.apple.com")
#     try:
#         connect.request("POST", "/verifyReceipt", pay_receipt, headers)
#         result = connect.getresponse()
#     except:
#         return Fail("验证失败,请联系客服")
#
#     if result.status != 200:
#         return Fail("验证失败,请联系客服")
#
#     data = result.read()
#     connect.close()
#     if data:
#         decodedJson = json.loads(data)
#         status = decodedJson.get('status')
#         receipt = decodedJson.get('receipt', {})
#         transaction_id = receipt.get('transaction_id', '')
#         # purchase_date = receipt.get('original_purchase_date', '')
#         # product_id = receipt.get('product_id', '')
#         if status == 0:
#             # 返回的status为0时代表支付是成功的，支付成功，最好记录一下
#             with DB() as db:
#                 db.sql_proc("sp_pay_notify", out_trade_no, transaction_id)
#                 db.commit()
#             return SUCCESS
#     return Fail("充值验证失败")


@post('/api/get_pay_way/')
def api_get_pay_way():
    """审核开关"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    version = p.__version
    game_no = p.__game_no
    show_ex = True
    ios_pay = True
    app_id = ''
    open_wx_pay = 1
    open_ali_pay = 1
    open_orgin_play = 1
    platform = ''
    try:
        with DB() as db:
            # r = db.sql_dict("select level from usr where usrid=%d;", p.uid)
            # if r['level'] < 5:
            #     return Success(PAY_WAY='IOS')
            r = db.sql_dict(""" select v.IS_APPROVE,c.open_wx_pay,c.open_ali_pay,c.open_orgin_play,c.platform
                                    from channel_version v 
                                    left join channel c on v.CHANNEL_ID=c.ID 
                                    where c.NO='%s' and v.NAME='%s'; """, game_no, version)
            r2 = db.sql_dict("""
                select app_id from channel where NO='%s';
            """, game_no)
            open_wx_pay = r['open_wx_pay']
            open_ali_pay = r['open_ali_pay']
            open_orgin_play = r['open_orgin_play']
        app_id = r2['app_id']
        if r and r.get('IS_APPROVE') == 0:
            # 国内ip 渠道非审核状态
            ios_pay = False
        platform = r['platform']
    except:
        ios_pay = True
        # LOG.exception('-------------api_get_pay_way--------------')
    if not open_wx_pay and not open_wx_pay:
        ios_pay = True
    # google
    if platform == 'ANDROID':
        ios_pay = False

    return Success(P="I" if ios_pay else "W",
                   A=app_id,
                   SEX=show_ex,
                   OPWX=open_wx_pay,
                   OPAL=open_ali_pay,
                   OPOP=open_orgin_play
                   )


USD_CACHE = None


@post('/api/get_lan_code/')
def api_get_lan_code():
    def get_usd_cny():
        import requests
        r = requests.get('http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXUSDCNY,'
                         '&column=code,price,UpdownRate&callback=ongetjsonpforex&_=1451543515359')
        s = re.findall("\((.*)\)", str(r.text))[0]
        sjson = json.loads(s)
        USDCNY = sjson["Data"][0][0][1] / 10000.0
        return USDCNY

    global USD_CACHE
    p = ParamWarper(request)
    version = p.__version
    game_no = p.__game_no
    TRACE("GET LAN CODE", version, game_no)
    with DB() as db:
        r = db.sql_dict("""select v.LAN_ID,v.IS_APPROVE,c.platform,c.ios_id,c.open_jump,c.jump_url from channel_version v 
                                      left join channel c on v.CHANNEL_ID=c.ID 
                                      where c.NO='%s' and v.NAME='%s'; """, game_no, version)
        lan_id = r['LAN_ID'] if r else 41

    if not USD_CACHE or not is_today(USD_CACHE['TIME']):
        USD_CACHE = {
            'TIME': datetime.datetime.now(),
            'USD': 6.8
        }

    return Success(RID=lan_id, AP=r['IS_APPROVE'], USD=USD_CACHE['USD'], ID=r['jump_url'] if r['open_jump'] else '')


@post('/api/pay_config/')
def api_pay_config():
    from sitecustomize import CUR_SERVER_ADDRESS
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    with DB() as db:
        r = db.sql_dict("select moneyconsume from usr where usrid=%d", p.uid)
        fp = 1 if r['moneyconsume'] == 0 else 0
        rs = db.sql_dict_array("select * from payconfig WHERE  PAYID<100100")
    if fp == 0: rs = [r for r in rs if r['PAYID'] != FISRT_PLAY_ID]
    if CUR_SERVER_ADDRESS == 'ggblg':
        for r in rs: r['RMB'] = r['USD']
    return {'data': rs, 'success': True, "fp": fp}


####################################################
# 兑换

@post('/api/api_exchange_config/')
def api_exchange_config():
    """兑换配置"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    with DB() as db:
        rs = db.sql_dict("select versionid from usr where usrid=%d", p.uid)
        versionid = rs['versionid']
        rs = db.sql_dict(
            'select lan_id from channel_version v left join channel  c on v.CHANNEL_ID=c.ID where c.NO="%s"', versionid)
        if rs['lan_id'] == 10:
            items = db.sql_dict_array(
                "SELECT ID, EN_NAME NAME, POINT, CHIPS, STOCK, LUCK_TYPE, RTYPE FROM exchange_config ORDER  BY ID")
        else:
            items = db.sql_dict_array(
                "SELECT ID, NAME, POINT, CHIPS, STOCK, LUCK_TYPE, RTYPE FROM exchange_config ORDER  BY ID")
        luck_draw_point = 1000
    return {
        'items': items,
        'luck_draw_point': luck_draw_point
    }


@post('/api/api_do_exchange/')
def api_do_exchange():
    """兑换实物"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    rtype = p.int__rtype
    address = p.str__address
    lxr = p.str__lxr
    phone = p.str__phone
    EN = False
    with DB() as db:
        rs = db.sql_dict("select versionid from usr where usrid=%d", p.uid)
        versionid = rs['versionid']
        if str(versionid).endswith('EN') or str(versionid).endswith('EN2'):
            EN = True

    if rtype == 2 and not all([address, lxr, phone]):
        return Fail("邮箱不能为空" if not EN else 'Email is empty')
    if lxr != phone:
        return Fail('两次输入邮箱不一致' if not EN else 'Email confrim fail')
    with DB() as db:
        rs = db.sql_dict("select LUCK_TYPE from exchange_config where ID=%d;", int(p.__exid))
        if rs['LUCK_TYPE'] not in [1, 3]:
            return Fail("不支持的兑换类型" if not EN else 'not support exchange type')
        db.sql_proc("sp_exchange_req", p.uid, p.int__exid, lxr, address, phone)
        db.commit()
    r = db.proc_result[0]
    if r['RESULT'] == 1:
        return Success(APPROVE_ID=['APPROVE_ID'])
    elif r['RESULT'] == -1:
        return Fail("积分不足" if not EN else 'credits not enough')
    elif r['RESULT'] == -2:
        return Fail("库存不足" if not EN else 'no stock')
    else:
        return Fail("请求失败清重试" if not EN else 'request fail')


@post('/api/api_do_luck_item/')
def api_do_luck_item():
    """抽取奖品"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    with DB() as db:
        rs = db.sql_dict_array(""" 
            SELECT
             ID,GET_RATE,NAME,RTYPE
            FROM
             exchange_config
            WHERE
             (LUCK_TYPE = 2 OR
              LUCK_TYPE = 3) AND
             (LIMIT_STOCK = 0 OR
              (LIMIT_STOCK = 1 AND
               STOCK > 0)) AND
             GET_RATE > 0
        """)
        wt = [r['GET_RATE'] for r in rs]
        ids = [r['ID'] for r in rs]

        extid = ids[weighted_choice(wt)]
        # extid=16
        db.sql_proc("sp_raw_luck_item", p.uid, extid)
        db.commit()

    r = db.proc_result[0]
    if r['RESULT'] == 1:
        return Success(APPROVE_ID=['APPROVE_ID'], EXID=extid)
    elif r['RESULT'] == -1:
        return Fail(p.string(1001))
    return Fail(p.string(1008))


@post('/api/api_do_luck_item_lxr_info/')
def api_do_luck_item_lxr_info():
    """填写联系人信息"""
    p = ParamWarper(request)
    address = p.str__address
    lxr = p.str__lxr
    phone = p.str__phone
    approve_id = p.__approve
    if not all([address, lxr, phone]):
        return Fail(p.string(1003))  # 地址联系人电话不能为空
    with DB() as db:
        r = db.sql_dict("""
            SELECT
             ID
            FROM
             exchange_approve_list
            WHERE
             ID = %d AND
             UID = %d
        """, approve_id, p.uid)
        if not r or r['ID'] != approve_id:
            return Fail(p.string(1004))  # 抽奖结果信息错误,请联系客服
        db.sql_exec("""
            UPDATE
             exchange_approve_list
            SET
             LXR   = '%s'
            ,ADDR  = '%s'
            ,PHONE = '%s'
            WHERE
             ID = %d
        """, lxr, address, phone, p.uid)
        return SUCCESS


@post('/api/api_exchange_status/')
def api_exchange_status():
    """审核状态列表"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    with DB() as db:
        return db.sql_array("""
        SELECT l.ID,
               l.CREATE_TIME,
               c.NAME,
               l.STATUS
        FROM exchange_approve_list l
             LEFT JOIN exchange_config c ON l.ID = c.ID
             LEFT JOIN usr u ON l.UID = u.usrid
        WHERE l.UID = %d
        """, p.uid)


@post('/api/api_gg_exchange_log/')
def api_gg_exchange_log():
    """GG兑换日志"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    with DB() as db:
        rs = db.sql_dict("select versionid from usr where usrid=%d", p.uid)
        versionid = rs['versionid']
        rs = db.sql_dict(
            'select lan_id from channel_version v left join channel  c on v.CHANNEL_ID=c.ID where c.NO="%s"', versionid)
        if rs['lan_id'] == 10:
            return db.sql_array("""
            SELECT l.ID,
                   l.EXTIME CREATE_TIME,
                   c.EN_NAME NAME,
                   '已发放' STATUS
            FROM exchange_log l
                 LEFT JOIN exchange_config c ON l.EXID = c.ID
            WHERE l.UID = %d and l.EXTYPE='积分兑换'
            """, p.uid)

        else:
            return db.sql_array("""
            SELECT l.ID,
                   l.EXTIME CREATE_TIME,
                   c.NAME,
                   '已发放' STATUS
            FROM exchange_log l
                 LEFT JOIN exchange_config c ON l.EXID = c.ID
            WHERE l.UID = %d and l.EXTYPE='积分兑换'
            """, p.uid)


@post('/api/api_luck_draw_history_list/')
def api_luck_draw_history_list():
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR

    with DB() as db:
        rs = db.sql_dict("select versionid from usr where usrid=%d", p.uid)
        versionid = rs['versionid']
        rs = db.sql_dict(
            'select lan_id from channel_version v left join channel  c on v.CHANNEL_ID=c.ID where c.NO="%s"', versionid)
        if rs['lan_id'] == 10:
            return db.sql_array("""
                SELECT
                u.usrid UID
                ,u.nickname NICKNAME
                ,e.EXTIME
                ,c.EN_NAME NAME
                FROM
                 exchange_log e
                 LEFT JOIN usr u ON e.UID = u.usrid
                 LEFT JOIN exchange_config c ON e.EXID = c.ID
                WHERE
                 e.EXTYPE = '积分抽奖' AND
                 e.EXTIME > f_today_min()  ORDER  BY   e.EXTIME DESC 
            """)

        return db.sql_array("""
            SELECT
            u.usrid UID
            ,u.nickname NICKNAME
            ,e.EXTIME
            ,c.NAME
            FROM
             exchange_log e
             LEFT JOIN usr u ON e.UID = u.usrid
             LEFT JOIN exchange_config c ON e.EXID = c.ID
            WHERE
             e.EXTYPE = '积分抽奖' AND
             e.EXTIME > f_today_min()  ORDER  BY   e.EXTIME DESC 
        """)


@post('/api/api_upload_avastar_notify/')
def api_upload_avastar_notify():
    """头像审核"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    if not p.__image_url: return Fail(p.string(1005))  # 参数错误
    image_url = "http://zrbjl.billionocean.cn/approve/" + p.__image_url
    TRACE("api_upload_avastar_notify:", image_url)
    with DB() as db:
        db.sql_exec("""delete from avastar_approve where uid=%d""", p.uid)
        db.sql_exec("""
            INSERT INTO poker.avastar_approve
            (IS_APPROVE, IMAGE_URL, UPLOAD_TIME,UID) 
            VALUES (0, '%s', now(),%d);
        """, image_url, p.uid)
        db.commit()
    return SUCCESS


@post('/api/api_facebook_bind/')
def api_facebook_bind():
    """玩家第一次用facebook登录，或者游客第一次绑定facebook账号，则给予玩家一次性奖励"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    fbid = str(p.__fbid).strip()  # facebookid
    # im = str(p.__im).strip()  #
    # nickname = str(p.__nickname).strip()  #
    with DB() as db:
        r = db.sql_dict("select usrid from usr where openid='%s';", fbid)
        if r and r.get('usrid'):
            return Success(p.string(1006), CODE=-2)  # 账号已经绑定
        else:
            GOLD = 50000
            db.sql_exec("""
            update usr set openid='%s',passporttype='facebook' ,chips=chips+%d
            where usrid=%d;
            """, fbid, GOLD, p.uid)
            db.commit()
            return Success(CODE=1, GOLD=GOLD)


@post('/api/api_facebook_bind_new/')
def api_facebook_bind():
    """玩家第一次用facebook登录，或者游客第一次绑定facebook账号，则给予玩家一次性奖励"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    fbid = str(p.__fbid).strip()  # facebookid
    fbtoken = str(p.__fbtoken).strip()  #
    # nickname = str(p.__nickname).strip()  #
    with DB() as db:
        r = db.sql_dict("select usrid from usr where openid='%s';", fbid)
        if r and r.get('usrid'):
            return Success(p.string(1006), CODE=-2)  # 账号已经绑定
        else:
            GOLD = 50000
            db.sql_exec("""
            update usr set openid='%s',passporttype='facebook' ,chips=chips+%d,token='%s'
            where usrid=%d;
            """, fbid, GOLD, fbtoken, p.uid)
            db.commit()
            return Success(CODE=1, GOLD=GOLD)


@post('/api/api_facebook_is_bind/')
def api_facebook_is_bind():
    """facebook 是否绑定"""
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    with DB() as db:
        r = db.sql_one("select usrid from usr where usrid=%d and passporttype='facebook';", p.uid)
        if r:
            return Success(CODE=1)
        else:
            return Success(CODE=0)


####################################################
@post('/api/api_tranimage_from_url/')
def api_tranimage_from_url():
    """转换圆角图片"""
    from common.oss import trans_net_image_url
    p = ParamWarper(request)
    if not p.uid: return TOKEN_ERROR
    image_url = p.__image_url
    with DB() as db:
        r = db.sql_dict("SELECT dest_img from img_url where src_img='%s';", image_url)
    if r and r['dest_img']:
        return Success(data=r['dest_img'])
    new_img_url = trans_net_image_url(p.uid, image_url)
    if new_img_url:
        with DB() as db:
            db.sql_exec("insert into img_url(src_img,dest_img) values('%s','%s');", image_url, new_img_url)
            db.commit()
    return Success(data=new_img_url)


PSS_APP_KEY = 'sandbox_0b14b5ad2fcd7f8d'
PSS_SECRET_KEY = '6bf7788d3e80b00f7428a5d553fd74e7'


@post('/api/payssion_notify_url/')
def api_payssion_notify_url():
    import hashlib
    p = ParamWarper(request)
    TRACE("REQ:", str(request.body))
    pm_id, amount, currency, order_id, state = p.__pm_id, p.__amount, p.__currency, p.__order_id, p.__state
    # api_key|pm_id|amount|currency|order_id|state|sercret_key
    verify = '|'.join([str(x) for x in [PSS_APP_KEY, pm_id, amount, currency, order_id, state, PSS_SECRET_KEY]])
    TRACE("BEFORE:", verify)
    verify = hashlib.md5(verify).hexdigest()
    TRACE("VERIFY:", verify)
    TRACE("SIGN:", p.__notify_sig)
    out_trade_no, transaction_id = order_id, p.__transaction_id
    if str(verify).lower() != str(p.__notify_sig).lower():
        TRACE("PARAM", pm_id, amount, currency, order_id)
        return error(404)
    if p.__state == 'completed':
        with DB() as db:
            db.sql_exec("""
                INSERT INTO poker.paycallback
                (TRANID, PAYID) 
                VALUES ('%s', '%s');
            """, transaction_id, out_trade_no)
            db.commit()
    return HTTPResponse("success", content_type="text/xml")




@route('/api/mycard_auth_code/', method=['GET', 'POST'])
def mycard_auth_code():
    try:
        p = ParamWarper(request)
        if p.__SandBoxMode=='true':
            MYCARD_URL = 'https://test.b2b.mycard520.com.tw/MyBillingPay/api/AuthGlobal'
        else:
            MYCARD_URL = 'https://b2b.mycard520.com.tw/MyBillingPay/api/AuthGlobal'
        param={
            'FacServiceId' : p.__FacServiceId,
            'FacTradeSeq' : p.__FacTradeSeq,
            'TradeType' : p.__TradeType,
            'ServerId' : p.nstr__ServerId,
            'CustomerId' : p.__CustomerId,
            'PaymentType' : p.nstr__PaymentType,
            'ItemCode' : p.nstr__ItemCode,
            'ProductName' : p.__ProductName,
            'Amount' : p.__Amount,
            'Currency' : p.__Currency,
            'SandBoxMode' : p.__SandBoxMode,
            'Hash' : p.__Hash
        }

        MYCARD_URL+="?FacServiceId={FacServiceId}&FacTradeSeq={FacTradeSeq}&TradeType={TradeType}&ServerId={ServerId}&CustomerId={CustomerId}&PaymentType={PaymentType}&ItemCode={ItemCode}&ProductName={ProductName}&Amount={Amount}&Currency={Currency}&SandBoxMode={SandBoxMode}&Hash={Hash}"
        MYCARD_URL=MYCARD_URL.format(**param)
        TRACE("MYCARDURL:",MYCARD_URL)
        r=requests.get(MYCARD_URL)
        return HTTPResponse(r.text, content_type="text/xml")
    except Exception,e:
        TRACE_ERROR(e)

@post('/api/mycard_notify_url/')
def mycard_notify_url():
    p = ParamWarper(request)
