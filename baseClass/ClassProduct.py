import datetime

import pandas as pd


# 定一个 Product 类
class Product:
    # 初始化，条码，名称、所属店铺
    def __init__(self, barcode, Shop):
        self.barcode = barcode
        self.Shop = Shop

    # 计算商品若干天以来的日均销售量（tan值）
    def get_tan(self, days):
        # 查询最近若干天以来的销量
        sales = self.sales_recent(days)
        # 计算tan值
        tan = sales / days
        return tan

    # 商品名称属性
    @property
    def name(self):
        # 根据productBarcode到数据表中查询最新的订单记录，并返回productName
        from mydb_fix import conn
        sql = 'select productName from SaleRecords2 where productBarcode = "{}" order by time desc limit 1'.format(
            self.barcode)
        df = pd.read_sql(sql, conn)
        return df.iloc[0, 0]

    @property
    def pid(self):
        return self.Shop.get_product_id(self.barcode)

    @property
    def find_product(self):
        return self.Shop.find_product(self.barcode)

    # 查询最近若干天以来的销量
    def sales_recent(self, days):
        from datetime import datetime as dt
        from mydb_fix import conn
        # 查询最近若干天以来的销量
        sql = '''
        SELECT SUM(productQuantity) AS sales    -- 汇总销量 productQuantity
        FROM SaleRecords2
        WHERE productBarcode = '{}'
        AND time BETWEEN '{}' AND '{}'
        '''.format(self.barcode, dt.now() - datetime.timedelta(days=days), dt.now())
        # print(sql)
        df = pd.read_sql(sql, conn)
        count = df.iloc[0, 0]
        return count  # 返回销量

    # 到数据表中查询商品某一天的销量，默认为今天
    def get_sales(self, date=None, end_date=None):
        from datetime import datetime as dt
        from mydb_fix import conn
        if date is None:
            begin_date_time = dt.now().strftime('%Y-%m-%d') + ' 00:00:00'
            end_date_time = dt.now().strftime('%Y-%m-%d') + ' 23:59:59'
        else:
            if end_date is None:
                begin_date_time = date + ' 00:00:00'
                end_date_time = date + ' 23:59:59'
            else:
                begin_date_time = date + ' 00:00:00'
                end_date_time = end_date + ' 23:59:59'

        # 根据条码、店铺、日期查询记录，并汇总销量productQuantity
        sql = '''
        SELECT SUM(productQuantity) AS sales    -- 汇总销量 productQuantity
        FROM SaleRecords2
        WHERE productBarcode = '{}'
        AND store = '{}'
        AND time BETWEEN '{}' AND '{}'
        '''.format(self.barcode, self.Shop.name, begin_date_time, end_date_time)
        # print(sql)
        df = pd.read_sql(sql, conn)
        count = df.iloc[0, 0]
        return count  # 返回销量

    # 查询商品今日的库存波动情况
    def get_stock_change(self, date='', end_date=''):
        __table = self.Shop.get_sale_records_by_dates(date, end_date)
        __table = __table[__table['productBarcode'] == self.barcode]
        # 检查table是否为空dt
        if __table.empty:
            print('在指定日期{}没有查询到该商品的销售记录'.format(date))
            return 0, 0
        else:
            sale_count = __table['productQuantity'].sum()
            stock = __table.sort_values(by='time', ascending=False).iloc[0]['productStock']
            if stock < 0:
                wave_percent = int(sale_count / (sale_count + 0) * 100)
            else:
                wave_percent = int(sale_count / (sale_count + stock) * 100)
            return {'stock': stock, 'sale_count': sale_count, 'wave_percent': wave_percent}
