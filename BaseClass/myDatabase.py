import sqlite3
import pandas as pd
import os

if os.name == 'posix':
    dbpath = '/Users/mengmeng/Documents/Python_Projects/MMSD_V0.2/BaseClass/mmsd.db'
else:
    dbpath = "C:\\Users\\mengmeng\\Documents\\Python_Projects\\mmsd.db"

conn = sqlite3.connect(dbpath)


class ShopDb(object):

    # 初始化数据库con和cursor
    def __init__(self, shop_id, shop_name):
        self.conn = sqlite3.connect(dbpath)  # 创建数据库连接
        self.cursor = self.conn.cursor()  # 创建游标
        self.shop_id = shop_id                # 指定店铺id
        self.shop_name = shop_name            # 指定店铺名

    # 关闭数据库
    def close(self):
        self.conn.close()

    # 做一个查询最近销售时间的操作,根据shop_name和barcode
    def query_last_sale_time(self, barcode):
        sql = "select time from SaleRecords where store = '%s' and productBarcode = '%s'" % (self.shop_name, barcode)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    # 做一个SaleRecords表 实时订单记录更新函数
    def update_records(self):
        print('----更新数据表 SaleRecords ----')
        from datetime import datetime
        # 获取库中最新的记录的时间'time',设为beginDateTime，当前时间设为endDateTime，获取订单记录
        beginDateTime = conn.execute("SELECT time FROM SaleRecords2 ORDER BY time DESC LIMIT 1").fetchone()[0]
        endDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print('beginDateTime: ', beginDateTime)
        print('endDateTime: ', endDateTime)

        from 外部接口.pos_login import get_zd_session
        zd_session = get_zd_session()
        # 获取订单记录
        __url = "https://beta47.pospal.cn/Report/LoadProductSaleDetailsByPage"
        resp = zd_session.post(url=__url,
                               data={
                                   'beginDateTime': beginDateTime,
                                   'endDateTime': endDateTime,
                                   'asc': "false",
                                   'categorysJson': "[]"
                               })

        # 将resp.json()['contentView'] 转为beautifulsoup对象,逐行插入数据库
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.json()['contentView'], 'html.parser')

        # 读取行数据
        for tr in soup.find_all('tr')[1:]:
            # 读取每个td
            tds = tr.find_all('td')
            # 如果_id tds[0]，在数据表中已经存在，则跳过
            if conn.execute("SELECT _id FROM SaleRecords2 WHERE _id = ?", (tds[0].text,)).fetchone() is not None:
                continue
            # 将每个td的文本内容转为一整个字符串
            tds = [td.text.strip() for td in tds[1:]]
            # 将tds的内容插入数据表
            conn.execute("INSERT OR IGNORE INTO SaleRecords2 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         tds)
            conn.commit()
            print('写入一条记录 _id: ', tds[0])
        print('更新完成!')
        print('-' * 50)
        return '成功'


def completeDb():
    # 完成数据库的初始化
    from BaseClass.Shop import gtpShop, syhShop
    from datetime import datetime as dt
    from datetime import timedelta

    conn = sqlite3.connect(dbpath)
    for i in range(20):
        endDateTime = dt.now().replace(hour=23) - timedelta(days=(i * 30))
        beginDateTime = endDateTime - timedelta(days=((i + 1) * 30))
        df1 = gtpShop.pos.LoadProductSaleDetailsByPage(beginDateTime=beginDateTime.strftime('%Y-%m-%d'),
                                                       endDateTime=endDateTime.strftime('%Y-%m-%d'))
        print(df1)
        df1.astype(str).to_sql('SaleRecords', conn, if_exists='append', index=False)


completeDb()
