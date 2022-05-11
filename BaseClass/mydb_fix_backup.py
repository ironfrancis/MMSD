import sqlite3
import pandas as pd

# 打开数据库
# conn = sqlite3.connect('/Users/mengmeng/Documents/Python_Projects/mydatabase.db')


# 创建数据表
def create_table():
    colsList = ['流水号', '销售时间', '销售门店', '会员姓名', '会员卡号', '导购员', '商品名称', '商品条码', '货号', '规格', '单位', '商品分类', '品牌',
                '现有库存', '商品原价', '商品折后价', '销售数量', '商品总价', '实收金额', '销售额占比', '成本', '利润', '利润率']

    conn.execute('''CREATE TABLE SaleRecords2
                    (
                    _id text PRIMARY KEY,
                    time datetime,
                    store TEXT,
                    memberName TEXT,
                    memberCard TEXT,
                    salesperson TEXT,
                    productName TEXT,
                    productBarcode TEXT,
                    productCode TEXT,
                    productSpec TEXT,
                    productUnit TEXT,
                    productCategory TEXT,
                    productBrand TEXT,
                    productStock FLOAT,
                    productPrice FLOAT,
                    productDiscountPrice FLOAT,
                    productQuantity INTEGER,
                    productTotalPrice FLOAT,
                    productReceived FLOAT,
                    productReceivedRate FLOAT,
                    cost FLOAT,
                    profit FLOAT,
                    profitRate FLOAT
                    )''')
    conn.commit()


# 检查数据表 SaleRecords2 的内容，使用pandas读取数据表，并输出
def check_table():
    df = pd.read_sql_query("SELECT * FROM SaleRecords2", conn)
    return df


# 删除数据表2
def drop_table():
    conn.execute("DROP TABLE SaleRecords2")


# 做一个SaleRecords表 实时订单记录更新函数
def update_records():
    print('----更新数据表 SaleRecords2 ----')
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


# 做一个根据时间范围查询收银后台并写入数据表的方法
def query_records_by_timeframe(beginDateTime, endDateTime):
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
    print(resp)
    # 将resp.json()['contentView'] 转为beautifulsoup对象,逐行插入数据库
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.json()['contentView'], 'html.parser')
    # 读取行数据
    for tr in soup.find_all('tr')[1:]:
        # 读取每个td
        tds = tr.find_all('td')
        # 将每个td的文本内容转为一整个字符串
        tds = [td.text.strip() for td in tds[1:]]
        # 将tds的内容插入数据表
        conn.execute("INSERT OR IGNORE INTO SaleRecords2 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     tds)
        print('写入一条记录 id: ', tds[0])
    conn.commit()

