# coding=utf-8
class Lan(object):
    # 10
    EN = {
        1001: "lack of integration",
        1002: "request failure please retry",
        1003: "address contact phone can't be empty",
        1004: "error of lottery result information, please contact customer service",
        1005: "parameter error",
        1006: "account has already bouned",
        1007: "lack of stock",
        1008: "request failure to retry",
        1009:"must recharge for the first time"
    }

    # 41
    ZH_CN = {
        1001: "积分不足",
        1002: "请求失败清重试",
        1003: "地址联系人电话不能为空",
        1004: "抽奖结果信息错误,请联系客服",
        1005: "参数错误",
        1006: "账号已经绑定",
        1007:"库存不足",
        1008:"请求失败清重试",
        1009:"必须首次充值",

    }

    def __init__(self, lan_id):
        self.lid = lan_id

    def string(self, msg_id):
        if self.lid == 10:
            return self.EN.get(msg_id)
        return self.ZH_CN.get(msg_id)
