import sqlite3
import pandas as pd
import os

import BaseClass.Pospal

if os.name == 'posix':
    dbpath = '/Users/mengmeng/Documents/Python_Projects/MMSD_V0.2/BaseClass/mmsd.db'
else:
    dbpath = "C:\\Users\\mengmeng\\Documents\\Python_Projects\\mmsd.db"

conn = sqlite3.connect(dbpath)


def completeDb():
    # 完成数据库的初始化
    from BaseClass.Shop import gtpShop, syhShop
    from datetime import datetime as dt
    from datetime import timedelta

    conn = sqlite3.connect(dbpath)
    for i in range(30):
        endDateTime = (dt.now().replace(hour=23) - timedelta(days=(i * 30)))
        beginDateTime = (endDateTime - timedelta(days=(30)))
        endDateTime = endDateTime.strftime('%Y-%m-%d') + ' 00:00:00'
        beginDateTime = beginDateTime.strftime('%Y-%m-%d') + ' 00:00:00'
        print(beginDateTime, endDateTime)
        session = BaseClass.Pospal.get_session(numbers='18014151457')
        url = 'https://beta47.pospal.cn/Report/LoadProductSaleDetailsByPage'
        data = {
            "keyword": "",
            'userIds': "['4455361','4151410']",
            "beginDateTime": beginDateTime,
            "endDateTime": endDateTime,
            "pageIndex": "1",
            "pageSize": "100000",
            "asc": "false",
            "categorysJson": "[]",
            "brandUids": "[]",
        }
        resp = session.post(url, data=data)  # 请求服务器
        table = resp.json()['contentView']  # 解析返回的json数据
        table = "<table>" + table + "</table>"  # 对内容修饰table标签
        table = pd.read_html(table, index_col="Unnamed: 0")[0]  # pandas读取table
        if table.shape[0] == 1:
            print("已经获取到最早到记录，结束运行！")
            break
        # 写入数据表
        table.to_sql('SaleRecords', conn, if_exists='append', index=False)

        print(table.shape[0])
        print("-" * 50)


# 启动时更新数据库
def updateDb():
    # 先获取数据库最新数据的时间标记
    print("-" * 50)
    print("开始更新数据库...")
    from datetime import datetime as dt
    from datetime import timedelta
    conn = sqlite3.connect(dbpath)
    endDateTime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    beginDateTime = conn.execute("SELECT 销售时间 FROM SaleRecords ORDER BY 销售时间 DESC LIMIT 1").fetchone()[0]
    print(beginDateTime, endDateTime)
    session = BaseClass.Pospal.get_session(numbers='18014151457')
    url = 'https://beta47.pospal.cn/Report/LoadProductSaleDetailsByPage'
    data = {
        "keyword": "",
        'userIds': "['4455361','4151410']",
        "beginDateTime": beginDateTime,
        "endDateTime": endDateTime,
        "pageIndex": "1",
        "pageSize": "100000",
        "asc": "false",
        "categorysJson": "[]",
        "brandUids": "[]",
    }
    resp = session.post(url, data=data)  # 请求服务器
    table = resp.json()['contentView']  # 解析返回的json数据
    table = "<table>" + table + "</table>"  # 对内容修饰table标签
    table = pd.read_html(table, index_col="Unnamed: 0")[0]  # pandas读取table
    # 读取最新的流水号
    last_id = conn.execute("SELECT 流水号 FROM SaleRecords ORDER BY 流水号 DESC LIMIT 1").fetchone()[0]
    table.drop(table[table['流水号'] == last_id].index, inplace=True)
    print(table)
    # 写入数据表
    table.to_sql('SaleRecords', conn, if_exists='append', index=False)
    print(table.shape[0], "条记录更新完成！")
    print("-" * 50)
    conn.commit()
    conn.close()


class ShopDb(object):

    # 初始化数据库con和cursor
    def __init__(self, shop_id, shop_name):
        self.conn = sqlite3.connect(dbpath)  # 创建数据库连接
        self.cursor = self.conn.cursor()  # 创建游标
        self.shop_id = shop_id  # 指定店铺id
        self.shop_name = shop_name  # 指定店铺名

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


updateDb()
