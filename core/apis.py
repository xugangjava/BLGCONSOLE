# coding=utf-8

from core.api import *

@post('/do/')
def go(code):
    # 注册
    if code == "api_sms_register_sms_code":
        """发送注册验证码"""
        return api_sms_register_sms_code()
    #######################################################
    # 找回密码
    elif code == "api_sms_find_password":
        """找回密码验证码"""
        return api_sms_find_password()
    elif code == "api_player_reset_password":
        """重置密码"""
        return api_player_reset_password()

    #######################################################
    elif code=="api_sms_bind_user":
        """绑定账号"""
        return api_sms_bind_user()

    elif code=="api_player_is_bind":
        """账号是否绑定"""
        return api_player_is_bind()

    elif code=="api_player_bind_account":
        """绑定账号"""
        return api_player_bind_account()

    # 支付
    elif code=="api_h5_alipay_create_order":
        """创建订单"""
        return api_h5_alipay_create_order()

    elif code=="api_h5_wx_create_order":
        """创建微信订单"""
        return api_h5_wx_create_order()

    elif code=="api_get_pay_way":
        """审核开关"""
        return api_get_pay_way()

    elif code=="api_pay_config":
        return api_pay_config()

    ####################################################
    # 兑换
    elif code=="api_exchange_config":
        """兑换配置"""
        return api_exchange_config()

    elif code=="api_do_exchange":
        """兑换实物"""
        return api_do_exchange()

    elif code=="api_do_luck_item":
        """抽取奖品"""
        return api_do_luck_item()

    elif code=="api_do_luck_item_lxr_info":
        """填写联系人信息"""
        return api_do_luck_item_lxr_info()

    elif code=="api_exchange_status":
        """审核状态列表"""
        return api_exchange_status()

    elif code=="api_luck_draw_history_list":
        return api_luck_draw_history_list()

    elif code=="api_upload_avastar_notify":
        """头像审核"""
        return api_upload_avastar_notify()

    elif code=="api_get_lan_code":
        """语言编号"""
        return api_get_lan_code()
        ####################################################


# 注册
@post('/0F67ABF10C62C21CF845339C5578AFC2/')  # sms_register_sms_code
def md5api_sms_register_sms_code():
    """发送注册验证码"""
    return api_sms_register_sms_code()


#######################################################
# 找回密码
@post('/DEDBFB9BF4E269E572A3408B759CB2F7/')  # sms_find_password
def md5api_sms_find_password():
    """找回密码验证码"""
    return api_sms_find_password()


@post('/D33DB549A021AF79DE6E9A28D375938C/')  # player_reset_password
def md5api_player_reset_password():
    """重置密码"""
    return api_player_reset_password()


#######################################################
@post('/2653D26B9360F96EB4ECCB28B8782C3E/')  # sms_bind_user
def md5api_sms_bind_user():
    """绑定账号"""
    return api_sms_bind_user()


@post('/64E53199095E7C98A332715DB651BE2D/')  # player_is_bind
def md5api_player_is_bind():
    """账号是否绑定"""
    return api_player_is_bind()


@post('/090E9BD26112B054969F4C58E36C3066/')  # player_bind_account
def md5api_player_bind_account():
    """绑定账号"""
    return api_player_bind_account()


# 支付
@post('/5273231C65EE662E48847B0C631CD912/')  # h5_alipay_create_order
def md5api_h5_alipay_create_order():
    """创建订单"""
    return api_h5_alipay_create_order()


@post('/CA53D2D42D5B584E2219E7D4E51DEEE8/')  # h5_wx_create_order
def md5api_h5_wx_create_order():
    """创建微信订单"""
    return api_h5_wx_create_order()


@get('/6DF0BAD46456785D16A5700BFEDA25EF/')  # h5_wx_pay_url
@view('wx_pay_url.html')
def md5api_h5_wx_pay_url():
    return api_h5_wx_pay_url()


@get('/988F384EE1CD3808091EF477C27CF559/')  # h5_wx_pay_redirect_url
@view('wx_pay_url.html')
def md5api_h5_wx_pay_redirect_url():
    return api_h5_wx_pay_redirect_url()


@post('/42863F62F14BF1254867F7C7F06779F1/')  # aplipay_notify_url
def md5api_aplipay_notify_url():
    """支付宝回调"""

    return api_aplipay_notify_url()


@post('/B341FEC6D00AC2D8C1075724C3FB68D3/')  # wxpay_notify_url
def md5api_wxpay_notify_url():
    """微信回调"""
    return api_wxpay_notify_url()


@post('/8B8F5C6F9B2883D48CE5726CA4657227/')  # get_pay_way
def md5api_get_pay_way():
    """审核开关"""
    return api_get_pay_way()


@post('/BDAFD06ADC96F111A233072FBD7A2460/')  # pay_config
def md5api_pay_config():
    return api_pay_config()


####################################################
# 兑换
@post('/BAEE754A9B3FF393DC4F6E2AB61589FF/')  # api_exchange_config
def md5api_exchange_config():
    """兑换配置"""
    return api_exchange_config()


@post('/FCA06CDF9F1C8AEF866049F1A6FB4DC2/')  # api_do_exchange
def md5api_do_exchange():
    """兑换实物"""
    return api_do_exchange()


@post('/E309314F25D66513C5E256CC03528A9D/')  # api_do_luck_item
def md5api_do_luck_item():
    """抽取奖品"""
    return api_do_luck_item()


@post('/7A8806A011E0BD467E4A2B0DDA4F52CD/')  # api_do_luck_item_lxr_info
def md5api_do_luck_item_lxr_info():
    """填写联系人信息"""
    return api_do_luck_item_lxr_info()


@post('/EA6AED28D4EFCFB379A0E09C283E30FB/')  # api_exchange_status
def md5api_exchange_status():
    """审核状态列表"""
    return api_exchange_status()


@post('/1B173E702459C99FD3E6CCB787DEF911/')  # api_luck_draw_history_list
def md5api_luck_draw_history_list():
    return api_luck_draw_history_list()


@post('/4BCF6317B9C463240650D0580F38141A/')  # api_upload_avastar_notify
def md5api_upload_avastar_notify():
    """头像审核"""
    return api_upload_avastar_notify()


@post('/71324D7D8D7580F04226847B036FC324/')  # get_lan_code
def md5api_get_lan_code():
    return api_get_lan_code()

####################################################
#google 支付
@post('/9027572CD027AA1591D599D8B6ECFBB2/')  # api_google_play_create_order
def md5api_google_play_create_order():
    """头像审核"""
    return api_google_play_create_order()

@post('/B4DE4E366BFEFC6865DA5D3232BDCE96/')  # api_google_play_callback
def md5api_google_play_callback():
    return api_google_play_callback()

@post('/8788C2194D61B22B4990FE539276EA0D/')  # api_facebook_bind
def md5api_facebook_bind():
    return api_facebook_bind()

@post('/5A1EE2B6046BD103686288BC6879C053/')  # api_facebook_is_bind
def md5api_facebook_is_bind():
    return api_facebook_is_bind()

####################################################
@post('/apitrancimage/')#get_lan_code
def md5api_tranimage_from_url():
    return api_tranimage_from_url()