# coding=utf-8


# 发送验证码
import base64
import datetime
import ssl
import urllib2
from xml.dom import minidom

from server_conf import DEBUG

ssl._create_default_https_context = ssl._create_unverified_context
import md5 as MD5


# 返回签名
def getSig(accountSid, accountToken, timestamp):
    sig = accountSid + accountToken + timestamp
    return MD5.new(sig).hexdigest().upper()


# 生成授权信息
def getAuth(accountSid, timestamp):
    src = accountSid + ":" + timestamp
    return base64.encodestring(src).strip()


import sys

coding_type = sys.getfilesystemencoding()


# 发起http请求
def urlOpen(req, data=None):
    try:

        res = urllib2.urlopen(req, data)
        data = res.read()
        res.close()
    except urllib2.HTTPError, error:
        data = error.read()
        error.close()
    return data


# 生成HTTP报文
def createHttpReq(req, url, accountSid, timestamp, responseMode, body):
    req.add_header("Authorization", getAuth(accountSid, timestamp))
    if responseMode:
        req.add_header("Accept", "application/" + responseMode)
        req.add_header("Content-Type", "application/" + responseMode + ";charset=utf-8")
    if body:
        body = body.encode('utf-8')
        req.add_header("Content-Length", len(body))
        req.add_data(body)
    return req


# 参数意义说明
# accountSid 主账号
# accountToken 主账号token
# clientNumber 子账号
# appId 应用的ID
# clientType 计费方式。0  开发者计费；1 云平台计费。默认为0.
# charge 充值或回收的金额
# friendlyName 昵称
# mobile 手机号码
# isUseJson 是否使用json的方式发送请求和结果。否则为xml。
# start 开始的序号，默认从0开始
# limit 一次查询的最大条数，最小是1条，最大是100条
# responseMode 返回数据个格式。"JSON" "XML"
# chargeType  0 充值；1 回收。
# fromClient 主叫的clientNumber
# toNumber 被叫的号码
# toSerNum 被叫显示的号码
# verifyCode 验证码内容，为数字和英文字母，不区分大小写，长度4-8位
# displayNum 被叫显示的号码
# templateId 模板Id
class RestAPI(object):
    HOST = "https://api.ucpaas.com"
    PORT = ""
    SOFTVER = "2014-06-30"
    JSON = "json"
    XML = "xml"

    # 短信验证码（模板短信）
    # accountSid 主账号ID
    # accountToken 主账号Token
    # appId 应用ID
    # toNumber 被叫的号码
    # templateId 模板Id
    # param <可选> 内容数据，用于替换模板中{数字}
    def templateSMS(self, accountSid, accountToken, appId, toNumbers, templateId, param, isUseJson=True):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        signature = getSig(accountSid, accountToken, timestamp)
        url = self.HOST + ":" + self.PORT + "/" + self.SOFTVER + "/Accounts/" + accountSid + "/Messages/templateSMS?sig=" + signature

        if isUseJson:
            body = '{"templateSMS":{ "appId":"%s","to":"%s","templateId":"%s","param":"%s"}}' % (
                appId, toNumbers, templateId, param)
            responseMode = self.JSON
        else:
            body = "<?xml version='1.0' encoding='utf-8'?>\
					<templateSMS>\
						<appId>%s</appId>\
						<to>%s</to>\
						<templateId>%s</templateId>\
						<param>%s</param>\
					</templateSMS>\
					" % (appId, toNumbers, templateId, param)
            responseMode = self.XML
        req = urllib2.Request(url)
        return urlOpen(createHttpReq(req, url, accountSid, timestamp, responseMode, body))



def sms_code(code, toNumber, operator):
    test = RestAPI()
    accountSid = "3e85715eaf1fdce6ab8a2bab5d12f32f"
    accountToken = "2288c0b5c6ab76e5c61d0ded88a9d1dc"
    appId = "22f2d222a0fa4455b9e6fe491c9fb63d"
    isUseJson = False
    templateId = '114897'
    param = operator + ',' + str(code)
    xml = test.templateSMS(accountSid, accountToken, appId, toNumber, templateId, param, isUseJson)
    if DEBUG:
        print xml
    try:
        r = minidom.parseString(xml)
        return r.getElementsByTagName('respCode')[0].childNodes[0].nodeValue == '000000'
    except:
        return False



#
#
# # 验证码提示
# def ffqp_sms_notify(req):
#     # p = ParamWarper(req)
#     return HttpResponse("success", content_type="text/plain")
#
#
# def ffqp_sms_code(req):
#     p = ParamWarper(req)
#     user_id = p.__user_id
#     game_no = p.__game_no
#     operator = p.__operator
#     phone = p.__phone
#     code = str(random.randint(1000, 9999))
#     if operator=='绑定账号' or operator=='账号注册':
#         with connection.cursor() as cursor:
#             if sql_exists(cursor,"SELECT 1 FROM dbo.TUsers WHERE UserName='%s'",phone):
#                 return Fail("该手机已绑定账号")
#     # user_id = str(user_id).strip("\"")
#     o = UserVerifyCode.objects.filter(uid=str(user_id)).first()
#     if not o:
#         o = UserVerifyCode(uid=str(user_id))
#     else:
#         if o.is_in_min:
#             return Fail("一分钟后才能发送验证码")
#
#     if _sms_code(code, phone, game_no, operator):
#         o.phone = str(phone)
#         o.code = code
#         o.send_time = datetime.datetime.now()
#         o.save()
#         return Success("发送成功")
#     else:
#         return Fail("验证码发送失败请重试")
#
#
# def ffqp_sms_cd(req):
#     p = ParamWarper(req)
#     user_id = p.int__user_id
#     if not check_token_vlidate(p):
#         return Fail("TOKEN验证失败")
#     o = UserVerifyCode.objects.filter(uid=str(user_id)).first()
#     if o:
#         return JObject(cd=o.cd_seconed)
#     else:
#         return JObject(cd=0)
#
#
# if __name__ == "__main__":
#     _sms_code("15902729415", 'ffqp', "", "123")
