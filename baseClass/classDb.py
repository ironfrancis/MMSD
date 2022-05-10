import sqlite3

dbpath = "/Users/mengmeng/Documents/MMSD V0.2/mydatabase.db"
conn = sqlite3.connect(dbpath)


class ShopDb(object):

    # 初始化数据库con和cursor
    def __init__(self, shop_id, shop_name):
        self.conn = sqlite3.connect(dbpath)   # 创建数据库连接
        self.cursor = self.conn.cursor()      # 创建游标
        self.shop_id = shop_id                # 指定店铺id
        self.shop_name = shop_name            # 指定店铺名

    # 关闭数据库
    def close(self):
        self.conn.close()

    # 做一个查询最近销售时间的操作,根据shop_name和barcode
    def query_last_sale_time(self, barcode):
        sql = "select time from SaleRecords2 where store = '%s' and productBarcode = '%s'" % (self.shop_name, barcode)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
