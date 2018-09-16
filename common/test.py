from core import DB, weighted_choice

if __name__ == '__main__':
    with DB() as db:
        rs = db.sql_dict_array("""
            SELECT
             ID,GET_RATE,NAME
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
        ids = [r['NAME'] for r in rs]
    result = {}
    for x in xrange(1000000):
        extid = ids[weighted_choice(wt)]
        if not extid in result: result[extid] = 0
        result[extid] = result[extid] + 1
    for k,v in result.iteritems():
        print str(k).encode('gbk').decode('gbk')+"="+str(v)