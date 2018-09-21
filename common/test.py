from core import DB, weighted_choice

if __name__ == '__main__':
    # # with DB() as db:
    # #     rs = db.sql_dict_array("""
    # #         SELECT
    # #          ID,GET_RATE,NAME
    # #         FROM
    # #          exchange_config
    # #         WHERE
    # #          (LUCK_TYPE = 2 OR
    # #           LUCK_TYPE = 3) AND
    # #          (LIMIT_STOCK = 0 OR
    # #           (LIMIT_STOCK = 1 AND
    # #            STOCK > 0)) AND
    # #          GET_RATE > 0
    # #     """)
    # #     wt = [r['GET_RATE'] for r in rs]
    # #     ids = [r['NAME'] for r in rs]
    # # result = {}
    # # for x in xrange(1000000):
    # #     extid = ids[weighted_choice(wt)]
    # #     if not extid in result: result[extid] = 0
    # #     result[extid] = result[extid] + 1
    # # for k,v in result.iteritems():
    # #     print str(k).encode('gbk').decode('gbk')+"="+str(v)
    # #
    # #
    # import hashlib
    # DATA="sandbox_0b14b5ad2fcd7f8d|1.00|USD|54d9b10d989b4e95b40e551facdf88df|6bf7788d3e80b00f7428a5d553fd74e7"
    #
    # SIGN="c58dad70dd556d2453f90efd30aacc03"
    # print "NOTIFY_SIGN", SIGN
    # print  "RESULT_SIGN", hashlib.md5(DATA).hexdigest()
    from common.pay import encode_url
    import hashlib
    data={
        'FacTradeSeq': '5qA6rmrVipdkixClEoXH',
        'ReturnCode': '1',
        'Hash': 'be69e32e03a4fbb949bf64c6dc76f9500cbea1f2a562adae61ac2b4eba805759',
        'PaymentType': 'COSTPOINT',
        'PromoCode': 'A0000',
        'Amount': '4.99',
        'submit1': 'Click here to continue if you are not automatically redirected.',
         'Currency': 'USD',
        'MyCardTradeNo': 'MMS1809210000151021',
        'PayResult': '3',
        'ReturnMsg': '%e7%b6%b2%e7%ab%99%e5%85%a7%e5%ae%b9%e5%95%8f%e9%a1%8c%e8%ab%8b%e6%b4%bd%e7%b6%b2%e7%ab%99%e5%ae%a2%e6%9c%8d%ef%bc%8c%e8%8b%a5%e7%82%ba%e4%ba%a4%e6%98%93%e5%95%8f%e9%a1%8c%e8%ab%8b%e6%92%a5%e6%89%93(02)26510754%e2%80%a7',
        'SerialId': '',
        'MyCardType': ''
    }
    FacTradeSeq = data['FacTradeSeq']
    ReturnCode = data['ReturnCode']
    Hash = data['Hash']
    PaymentType = data['PaymentType']
    PromoCode = data['PromoCode']
    Amount = data['Amount']
    Currency = data['Currency']
    PayResult = data['PayResult']
    ReturnMsg = data['ReturnMsg']
    MyCardTradeNo=data['MyCardTradeNo']
    MyCardType=data['MyCardType']
    PromoCode=data['PromoCode']
    MYCARDKEY = "At4qwWinp0cHizEmmX2qZPWW0jX0gXrl"
    PreHashValue = ReturnCode + PayResult + FacTradeSeq + PaymentType + Amount + Currency + MyCardTradeNo + MyCardType + PromoCode + MYCARDKEY

    print Hash
    sha256=hashlib.sha256()
    sha256.update(encode_url(PreHashValue))
    print sha256.hexdigest()