#!/usr/bin/env python
# coding: utf-8

import os
from datetime import datetime
from urllib import quote_plus, urlopen, urlencode

import xmltodict as xmltodict
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from server_conf import *
from core import *


class AliPay(object):
    PRIVATE_KEY = RSA.importKey(open(os.path.join(BASE_DIR, "rsa_private_key_pkcs8.pem")).read())
    PUB_KEY = RSA.importKey(open(os.path.join(BASE_DIR, "rsa_public_key.pem")).read())
    APP_ID = "2017022405859441"
    SELLER_ID = "finance@billionocean.cn"
    NOTIFY_URL = WEB_HOST + "api/aplipay_notify_url/"
    PID = "2088121623299027"

    @staticmethod
    def __ordered_data(data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据单独排序
        for key in complex_keys:
            data[key] = json.dumps(data[key], sort_keys=True).replace(" ", "")

        return sorted([(k, v) for k, v in data.items()])

    @staticmethod
    def sign_data_with_private_key(data):
        """
        通过如下方法调试签名
        方法1
            key = rsa.PrivateKey.load_pkcs1(open(self.__private_key_path).read())
            sign = rsa.sign(unsigned_string.encode("utf8"), key, "SHA-1")
            # base64 编码，转换为unicode表示并移除回车
            sign = base64.encodebytes(sign).decode("utf8").replace("\n", "")
        方法2
            key = RSA.importKey(open(self.__private_key_path).read())
            signer = PKCS1_v1_5.new(key)
            signature = signer.sign(SHA.new(unsigned_string.encode("utf8")))
            # base64 编码，转换为unicode表示并移除回车
            sign = base64.encodebytes(signature).decode("utf8").replace("\n", "")
        方法3
            echo "abc" | openssl sha1 -sign alipay.key | openssl base64
        """
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = AliPay.__ordered_data(data)
        unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)
        # 开始计算签名
        key = AliPay.PRIVATE_KEY
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA.new(unsigned_string.encode("utf8")))
        # base64 编码，转换为unicode表示并移除回车
        sign = base64.encodestring(signature).decode("utf8").replace("\n", "")
        return sign

    @staticmethod
    def create_pay_url(out_trade_no, total_amount, subject):

        data = {
            "app_id": AliPay.APP_ID,
            "method": "alipay.trade.wap.pay",
            "charset": "utf-8",
            "sign_type": "RSA",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "notify_url": AliPay.NOTIFY_URL,
            "biz_content": {
                "subject": subject,
                "out_trade_no": out_trade_no,
                "total_amount": total_amount,
                "product_code": "QUICK_MSECURITY_PAY"
            }
        }

        sign = AliPay.sign_data_with_private_key(data)
        ordered_items = AliPay.__ordered_data(data)
        quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in ordered_items)
        # 获得最终的订单信息字符串 各种语言都有DEMO
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return 'https://openapi.alipay.com/gateway.do?' + signed_string

    @staticmethod
    def create_app_trade(out_trade_no, total_amount, subject):

        data = {
            "app_id": AliPay.APP_ID,
            "method": "alipay.trade.app.pay",
            "charset": "utf-8",
            "sign_type": "RSA",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "notify_url": AliPay.NOTIFY_URL,
            "biz_content": {
                "subject": subject,
                "out_trade_no": out_trade_no,
                "total_amount": total_amount,
                "product_code": "QUICK_MSECURITY_PAY"
            }
        }
        return AliPay.create_trade(data)

    @staticmethod
    def create_trade(data):
        sign = AliPay.sign_data_with_private_key(data)
        ordered_items = AliPay.__ordered_data(data)
        quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in ordered_items)
        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    @staticmethod
    def verify_notify(data):
        params = {'partner': AliPay.PID, 'notify_id': data.get('notify_id')}
        gateway = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'
        verify_result = urlopen(gateway, urlencode(params)).read()
        return bool(verify_result.lower().strip() == 'true')


import requests
from xml.etree import ElementTree


def encode_url(url):
    import urllib
    url = url.decode('gbk', 'replace')
    return urllib.quote(url.encode('utf-8', 'replace'))


class WXPay(object):
    """微信支付，返回回客户端需要参数
    """
    APP_ID = "wx3ceddfeaaa501562"
    APP_SECRET = "6a8982cf03c463914659d6c0294238f2"
    MCHID = "1423863802"
    NOTIFY_URL = WEB_HOST + "wxpay_notify_url/"
    APIKEY = "RJcYjXX4DIrG8KKgbryyushZcDdJY7ay"

    def __init__(self, out_trade_no='', body='', total_fee=0, nonce_str='',
                 spbill_create_ip='8.8.8.8', trade_type='APP'):
        """
        :param out_trade_no: 订单ID
        :param body: 订单信息
        :param total_fee: 订单金额
        :param nonce_str: 32位内随机字符串
        :param spbill_create_ip: 客户端请求IP地址
        """
        self.params = {
            'appid': self.APP_ID,
            'mch_id': self.MCHID,
            'nonce_str': nonce_str,
            'body': body,
            'out_trade_no': str(out_trade_no),
            'total_fee': str(int(total_fee)),
            'spbill_create_ip': spbill_create_ip,
            'trade_type': trade_type,
            'notify_url': self.NOTIFY_URL
        }
        self.trade_type = trade_type
        self.url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'  # 微信请求url
        self.error = None

    def notify_xml_string_to_dict(self, xml_str):
        xml_data = xmltodict.parse(xml_str)['xml']
        params = {}
        for k in xml_data:
            params[k] = xml_data[k]
        return params

    def build_sign(self, p):
        # 对所有传入参数按照字段名的 ASCII 码从小到大排序（字典序）
        keys = p.keys()
        keys.sort()
        array = []
        for key in keys:
            # 值为空的参数不参与签名
            if p[key] is None or p[key] == '':
                continue
            # sign不参与签名
            if key == 'sign':
                continue
            array.append("%s=%s" % (key, p[key]))
        # 使用 URL 键值对的格式拼接成字符串string1
        string1 = "&".join(array)
        # 在 string1 最后拼接上 key=Key(商户支付密钥)得到 stringSignTemp 字符串
        stringSignTemp = string1 + '&key=' + self.APIKEY
        if DEBUG: print stringSignTemp
        # 对 stringSignTemp 进行 md5 运算，再将得到的字符串所有字符转换为大写
        m = hashlib.md5(stringSignTemp.encode('utf-8'))
        signed = m.hexdigest().upper()
        if DEBUG: print signed
        return signed

    def verify_notify(self, params):
        params = self.notify_xml_string_to_dict(params)
        notify_sign = params['sign']
        del params['sign']
        return self.build_sign(params) == notify_sign

    def get_sign(self, params):
        """生成sign"""
        sign = self.build_sign(params)
        params['sign'] = sign

    def _get_req_xml(self):
        """拼接XML """
        self.get_sign(self.params)
        xml = "<xml>"
        for k, v in self.params.items():
            v = v.encode('utf8')
            k = k.encode('utf8')
            xml += '<' + k + '>' + v + '</' + k + '>'
        xml += "</xml>"
        return xml

    def _get_prepay_id(self):
        """
        请求获取prepay_id
        """
        xml = self._get_req_xml()
        if DEBUG: print xml
        headers = {'Content-Type': 'application/xml'}
        r = requests.post(self.url, data=xml, headers=headers)
        re_text = r.text.encode(r.encoding)
        if DEBUG: print re_text
        re_xml = ElementTree.fromstring(re_text)

        xml_status = list(re_xml.iter('return_code'))[0].text
        if xml_status != 'SUCCESS':
            self.error = u"连接微信出错啦！"
            return
        prepay_id = list(re_xml.iter('prepay_id'))[0].text

        self.params['prepay_id'] = prepay_id
        self.params['package'] = 'Sign=WXPay'
        self.params['timestamp'] = str(int(time.time()))
        if self.trade_type == 'MWEB':
            self.mweb_url = list(re_xml.iter('mweb_url'))[0].text

    @staticmethod
    def gen_nonce_str():
        """
        生成随机字符串，有效字符a-zA-Z0-9

        :return: 随机字符串
        """
        return ''.join(str(uuid.uuid4()).split('-'))

    def proceed(self):
        """得到prepay_id后再次签名，返回给终端参数"""
        self._get_prepay_id()
        if self.error:
            return {}

        sign_again_params = {
            'appid': self.params['appid'],
            'noncestr': self.params['nonce_str'],
            'package': self.params['package'],
            'partnerid': self.params['mch_id'],
            'timestamp': self.params['timestamp'],
            'prepayid': self.params['prepay_id']
        }
        self.get_sign(sign_again_params)
        self.params['sign'] = sign_again_params['sign']

        # 移除其他不需要返回参数
        for i in self.params.keys():
            if i not in [
                'appid', 'mch_id', 'nonce_str',
                'timestamp', 'sign', 'package', 'prepay_id', 'mweb_url']:
                self.params.pop(i)
        return self.params


class H5WXPlay(WXPay):
    APP_ID = "wxc8aa03b5452bc816"
    APP_SECRET = "cbb6efe1c82089ada75fda0a027ef176"
    MCHID = "1447115402"
    NOTIFY_URL = WEB_HOST + "api/wxpay_notify_url/"
    APIKEY = "Qk4EhVG5pH85tk97dzxOFS4ZwH3PddZx"


def _check_pay_count(p):
    total_fee = p.__total_fee
    gold = p.__gold
    for p in PAY_CONFIG:
        if p['count'] == gold and total_fee == p['price'] * 100:
            return True
    return False


def get_client_ip(request):
    try:
        if request.environ.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.environ['REMOTE_ADDR']
        return ip
    except:
        return '8.8.8.8'


def _get_ip_country(ip):
    req = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=" + ip
    r = requests.get(req)
    j = r.json()
    TRACE(j)
    return j['country']


def get_client_ip_in_china(request):
    try:
        if request.environ.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.environ['REMOTE_ADDR']
        return _get_ip_country(ip) in ('中国', u'中国')
    except:
        return True


if __name__ == '__main__':
    print  _get_ip_country('59.174.226.223')
