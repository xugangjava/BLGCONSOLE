# coding=utf-8
import base64

import MySQLdb
from DBUtils.PooledDB import PooledDB

from server_conf import DB_PWD, TRACE
from tran import *

pool = PooledDB(MySQLdb, 5,
                host='localhost',
                user='root',
                charset='utf8',
                passwd=DB_PWD,
                db='poker',
                port=3306)


class ParamWarper(object):
    """
        try 是否包含参数返回boolean 返回参数或者None
        tryb  是否包含参数返回boolean
        b64 用b64解码
        json  用json解码
        trim 去掉空格
        time 时间参数
        date 日期参数
        list 列表参数
        ids int id 数组
    """

    def __init__(self, request, auth=False):
        self.request = request
        self.ispost = request.method == "POST"
        self.isget = not self.ispost
        self.uid = None

        # if auth:
        #     with DB() as db:
        #         r = db.sql_dict("""
        #         SELECT  UID
        #         FROM    dbo.TAuth
        #         WHERE   TOKEN = '%s';
        #         """, self.__TOKEN)
        #     if r: self.uid = r['UID']
        m = self.try__m
        self.isadd = m == 'add'
        self.isedit = m == 'edit'
        self.isdel = m == 'del'
        self.islist = m == 'list'
        self.isview = m == 'view'
        self.session = request.environ.get('beaker.session')
        self.params = {}
        self.params.update(request.GET)
        self.params.update(request.POST)
        if 'TOKEN' in self.params and 'USRID' in self.params:
            with DB() as db:
                r = db.sql_dict("select usrid from usr where (token='%s' or pwd='%s') and usrid=%d;",
                                self.params['TOKEN'],
                                self.params['TOKEN'],
                                int(self.params['USRID']))
                self.uid = int(r['usrid']) if r  else 0
            if not self.uid: TRACE("TOKEN ERROR")
        if "LAN" in self.params:
            try:
                self.lan = Lan(int(self.params['LAN']))
            except:
                self.lan = Lan(41)

    def string(self, msgid):
        return self.lan.string(msgid)

    def set_to_object(self, obj):
        if 'fields' in self.params:
            for f in self.params['fields']:
                setattr(obj, f, getattr(self, '__' + str(f)))

    @property
    def session_uid(self):
        return self.session.get('uid')

    def __getattr__(self, item):
        if not '__' in item:
            return ParamWarper.__getattr__(self, item)
        req = self.request
        if item == 'values':
            return req.GET['values'].split(',')
        elif item == 'editvalues':
            return req.GET['editvalues'].split(',')
        if item.startswith('__'):
            head, item = '', item.strip('__')
        else:
            head, item = item.split('__')
        trys = 'try' in head
        tryb = 'tryb' in head  # 是否包含参数
        b64 = 'b64' in head
        isjson = 'json' in head
        trim = 'trim' in head
        time = 'time' in head
        date = 'date' in head
        islist = 'list' in head
        ids = 'ids' in head
        isint = 'int' in head

        nstr = 'nstr' in head
        v = None
        if tryb:
            return item in req.GET or item in req.POST
        if item in req.GET:
            if trys and item not in req.GET:
                return str(v)
            v = req.GET.getlist(item) if islist else req.GET[item]

        if item in req.POST:
            if trys and item not in req.POST:
                return str(v)
            v = req.POST.getlist(item) if islist else req.POST[item]

        if nstr and v is None:
            return ''

        if v:
            if ids:
                v = [int(x) for x in v.split(',')]
            else:
                if b64:
                    v = base64.decodestring(v)
                if isjson:
                    v = json.loads(v)
                if isint or (hasattr(v, 'isdigit') and v.isdigit()):
                    v = int(float(v))
                if trim:
                    v = str(v).replace('\n', '').replace('\r', '').strip()
                if time:
                    v = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')

                elif date:
                    v = datetime.datetime.strptime(v, '%Y-%m-%d')
        return v


# coding=utf-8
import hashlib
import uuid
import time
import datetime
import json


class zipmap(dict):
    def __setitem__(self, key, value):
        if not self.has_key(key):
            super(zipmap, self).__setitem__(key, [value])
        else:
            self[key].append(value)


def md5(v):
    return hashlib.md5(str(v)).hexdigest()


import random, string


def random_password(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


def trade_no():
    return "EX_PHONE_" + str(uuid.uuid1()).replace('-', '').upper()


def timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S')


class Callback(object):
    def __init__(self, rep, success, message):
        self.rep = rep
        self.success = success
        self.message = message


def is_this_week(dt):
    n = datetime.datetime.now()
    this_week_start_dt = (
        n - datetime.timedelta(days=n.weekday())).replace(hour=0, minute=0, second=0)
    this_week_end_dt = (n + datetime.timedelta(days=6 -
                                                    n.weekday())).replace(hour=23, minute=59, second=59)
    return this_week_start_dt < dt < this_week_end_dt


def DATA(*args, **kv):
    return {
        'success': True,
        'result': kv
    }


def Fail(message="", **kv):
    kv['message'] = str(message)
    kv['success'] = False
    return kv


def Success(message="", **kv):
    kv['message'] = str(message)
    kv['success'] = True
    return kv


def OK(**kv):
    return Success("", **kv)


SUCCESS = OK()

TOKEN_ERROR = Fail("TOKEN验证失败")
UNKOWNEN_ERROR = Fail("请求失败请重试")
PARAM_ERROR = Fail("参数错误")


def ipaddress(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip


def is_today(val):
    return is_day(val)


def is_day(val, diff=0):
    if not val:
        return False
    day = datetime.datetime.now() + datetime.timedelta(days=diff)
    return day.year == val.year and day.month == val.month and day.day == val.day


def get_day(diff_day=0):
    d = datetime.datetime.now().replace(hour=0, minute=0, second=0)
    return d + datetime.timedelta(days=diff_day)


def get_day_str(diff_day=0):
    d = datetime.datetime.now().replace(hour=0, minute=0, second=0)
    return str(d + datetime.timedelta(days=diff_day))[0:10]


def toady_min():
    return datetime.datetime.now().replace(hour=0, minute=0, second=0)


def today_max():
    return datetime.datetime.now().replace(hour=23, minute=59, second=59)


def guid():
    import uuid
    return str(uuid.uuid4()).replace('-', '')


import re


def is_number(n):
    regex = re.compile(r"^(-?\d+)(\.\d*)?$")
    return True if re.match(regex, n) else False


class Row(object):
    def __init__(self, x):
        self.__dict__.update(x)


class DB(object):
    cursor = None
    conn = None
    proc_result = None

    def __enter__(self):
        self.conn = pool.connection()
        self.cursor = self.conn.cursor()
        return self

    def commit(self):

        self.conn.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def sql_padding_start_limit(self, start, limit, tbName, columNames, orderBy='', condition=''):
        curPage, pageSize = (start / limit) + 1, limit
        return self.sql_padding(curPage, pageSize, tbName, columNames, orderBy, condition)

    def sql_o(self, sql, *args):
        d = self.sql_dict(sql, *args)
        if isinstance(d, dict): return Row(d)
        return None

    def sql_exists(self, sql, *args):
        self.sql_exec(sql, *args)
        row = self.cursor.fetchone()
        return row and len(row) > 0

    def sql_dict(self, sql, *args):
        self.sql_exec(sql, *args)
        columns = [column[0] for column in self.cursor.description]
        row = self.cursor.fetchall()
        if not len(row):
            return None
        row = row[0]
        return dict(zip(columns, row))

    def sql_exec(self, sql, *args):
        sql_string = sql % args
        TRACE(sql_string)
        self.cursor.execute(sql_string)

    def sql_proc(self, proc, *args):
        TRACE(proc, args)
        self.cursor.callproc(proc, args)
        if self.cursor.description:
            columns = [column[0] for column in self.cursor.description]
            self.proc_result = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        self.cursor.close()
        self.cursor = self.conn.cursor()

    def sql_dict_array(self, sql, *args):
        self.sql_exec(sql, *args)
        columns = [column[0] for column in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def sql_combo(self, sql, *args):
        return {'items': self.sql_dict_array(sql, *args)}

    def sql_array(self, sql, *args):
        return {'data': self.sql_dict_array(sql, *args), 'success': True}

    def sql_one(self, sql, *args):
        return {'data': self.sql_dict(sql, *args), 'success': True}

    def sql_no_padding(self, sql, *args):
        r = self.sql_dict_array(sql, *args)
        return {'items': r, "total": len(r)}

    def sql_padding(self, start, limit, tbName, columNames, orderBy='', condition=''):
        curPage, pageSize = (start / limit) + 1, limit
        self.sql_exec("call sp_page_split(%d,%d,'%s','%s','%s','%s')",
                      curPage, pageSize, tbName, columNames, orderBy, condition)
        columns = [column[0] for column in self.cursor.description]
        items = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        self.cursor.nextset()
        totalCount = self.cursor.fetchone()
        totalCount = totalCount[0]
        return {
            "items": items,
            "total": totalCount
        }

    def sql_padding_2(self, start, limit, tbName,autopk, columNames, orderBy='', condition=''):
        curPage, pageSize = (start / limit) + 1, limit
        self.sql_exec("call sp_page_split_2(%d,%d,'%s','%s','%s','%s','%s')",
                      curPage, pageSize, tbName, columNames, orderBy, condition,autopk)
        columns = [column[0] for column in self.cursor.description]
        items = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        self.cursor.nextset()
        totalCount = self.cursor.fetchone()
        totalCount = totalCount[0]
        return {
            "items": items,
            "total": totalCount
        }

DAY = 60 * 60 * 24
HOUR = 60 * 60
MIN = 60


# 获取多少秒
def get_time(d, default=None):
    if not d:
        return default
    import time
    return time.mktime(d.timetuple())


def weighted_choice(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i


def random_is_happen(rate):
    wt = [rate, 100 - rate]
    wtp = [1. * x / sum(wt) for x in wt]
    p = [random.normalvariate(1. / x, 1. / x / 3.) for x in wtp]
    minp = 1.e9
    minj = -1
    for j, pp in enumerate(p):
        if pp < minp:
            minp = pp
            minj = j
    return minj == 0


##############################################################
if __name__ == '__main__':
    lhj_big_or_small_bet_rate = (49, 45, 41, 38, 36, 34, 32)
    x1, x2, x3 = 0, 0, 0
    prev_r = -1
    max_same = 0
    win_count = 0
    for x in xrange(1000000):
        if win_count > 6: win_count = 6
        r = int(random_is_happen(lhj_big_or_small_bet_rate[win_count]))
        if r == 1:
            win_count += 1
        else:
            win_count = 0

        if prev_r == 1:
            if prev_r == r:
                x3 += 1
            else:
                x3 = 0
            if x3 > max_same:
                max_same = x3

        prev_r = r
        if r == 0:
            x1 += 1
        elif r == 1:
            x2 += 1
    print x1, x2, max_same
# r=alipay_rsa_sgin(unicode('a=123','utf-8'))
#     print r
#     print alipay_rsa_verify('a=123',r)



SAFEHASH = [x for x in "0123456789-abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


def compress_UUID():
    row = str(uuid.uuid4()).replace('-', '')
    safe_code = ''
    for i in xrange(10):
        enbin = "%012d" % int(bin(int(row[i * 3] + row[i * 3 + 1] + row[i * 3 + 2], 16))[2:], 10)
        safe_code += (SAFEHASH[int(enbin[0:6], 2)] + SAFEHASH[int(enbin[6:12], 2)])
    return safe_code


def random_is_happen(rate):
    wt = [rate, 100 - rate]
    wtp = [1. * x / sum(wt) for x in wt]
    p = [random.normalvariate(1. / x, 1. / x / 3.) for x in wtp]
    minp = 1.e9
    minj = -1
    for j, pp in enumerate(p):
        if pp < minp:
            minp = pp
            minj = j
    return minj == 0
