import sqlite3
import pandas as pd
import os

import BaseClass.Pospal

if os.name == 'posix':
    dbpath = '/Users/mengmeng/Documents/Python_Projects/mmsd.db'
else:
    dbpath = "C:\\Users\\mengmeng\\Documents\\Python_Projects\\mmsd.db"

conn = sqlite3.connect(dbpath)


# 销售记录的补全
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


# 充值记录补全
def completeDbRecharges():
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
        url = 'https://beta47.pospal.cn/CardReport/LoadRechargelogsByPage'
        data = {
            "userId": "['4455361','4151410']",
            "cashierUid": "",
            "guiderUid": "",
            "rechargeType": "",
            "payMethod": "",
            "beginDateTime": beginDateTime,
            "endDateTime": endDateTime,
            "pageIndex": "1",
            "pageSize": "10000",
            "orderColumn": "",
            "asc": "false"
        }
        resp = session.post(url, data=data)  # 请求服务器
        table = resp.json()['contentView']  # 解析返回的json数据
        table = "<table>" + table + "</table>"  # 对内容修饰table标签
        table = pd.read_html(table, index_col="Unnamed: 0")[0]  # pandas读取table
        print(table)
        if table.shape[0] == 1:
            print("已经获取到最早到记录，结束运行！")
            break
        # 写入数据表
        table.to_sql('RechargeRecords', conn, if_exists='append', index=False)

        print(table.shape[0])
        print("-" * 50)


# 启动时更新数据库
def updateDb():
    print("-" * 50)
    print("本地数据库更新：")
    saleRecordsUpdate()
    print("\n")
    rechargeRecordsUpdate()
    print("更新完成！")
    print("-" * 50)
    pass


# 更新销售记录
def saleRecordsUpdate():
    # 先获取数据库最新数据的时间标记
    print("销售记录数据库...")
    from datetime import datetime as dt
    from datetime import timedelta
    conn = sqlite3.connect(dbpath)
    endDateTime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    beginDateTime = conn.execute("SELECT 销售时间 FROM SaleRecords ORDER BY 销售时间 DESC LIMIT 1").fetchone()[0]
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
    if table.shape[0] == 0:
        return print("销售记录无需更新！最新记录时间：", beginDateTime)
    else:
        # 写入数据表
        table.to_sql('SaleRecords', conn, if_exists='append', index=False)
        print(table.shape[0], "条记录更新完成！")


# 更新充值记录
def rechargeRecordsUpdate():
    # 先获取数据库最新数据的时间标记
    print("更新充值记录数据库...")
    from datetime import datetime as dt
    from datetime import timedelta
    conn = sqlite3.connect(dbpath)
    endDateTime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    beginDateTime = conn.execute("SELECT 充值时间 FROM RechargeRecords ORDER BY 充值时间 DESC LIMIT 1").fetchone()[0]
    session = BaseClass.Pospal.get_session(numbers='18014151457')
    url = 'https://beta47.pospal.cn/CardReport/LoadRechargelogsByPage'
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
    table = table[table['充值时间'] != beginDateTime]
    if table.shape[0] <= 0:
        return print("充值记录无需更新! 最新记录时间", beginDateTime)
    else:
        table.to_sql('RechargeRecords', conn, if_exists='append', index=False)
        print(table.to_markdown(), '已写入！')


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
        sql = "select 销售时间 from SaleRecords where 销售门店 = '%s' and 商品条码 = '%s'" % (self.shop_name, barcode)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]


updateDb()