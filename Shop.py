import json
import time

from pyecharts.charts import Bar
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from mydb_fix import conn
from pos_login import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1280)


# 打印Shop类的所有方法
def print_methods(obj):
    print([method for method in dir(obj) if callable(getattr(obj, method))])


# 定义一个类，用来操作 我的商店
class Shop(object):
    def __init__(self, name, phone, user_id):
        self.name = name
        self.phone = phone
        self.user_id = user_id

    # 网店商品列表
    def eshopList(self):
        table = self.pos.LoadEshopProductsByPage()
        table = table[table['是否显示'] == '是']
        print(table.sort_values('销售价', ascending=False))

    # 根据本地数据库查询的接口
    @property
    def DataBase(self):
        from baseClass.classDb import ShopDb
        return ShopDb(shop_id=self.user_id, shop_name=self.name)

    # 超类ProCat接口
    def Cat(self, name):
        from classProCat import ProCat
        cat = ProCat(name=name, shopId=self.user_id, pos=self.pos)
        print("get Cat")
        return cat

    # 定义一个方法，用来生成商品检查表
    def productDailyCheck(self, to_typora=False, to_excel=False, to_html=False):
        # 建立一个空df用于保存结果信息
        attention_df = pd.DataFrame(columns=['条码', '商品名称', '分类', '售价', '库存', '销量', '关注事项：'])
        ori_df = self.pos.LoadProductSaleDetailsByPage()  # 读取原始销售流水记录
        barcodeList = ori_df['商品条码'].unique().astype(str).tolist()  # 获取商品条码列表
        ignore_product_list = ['159869458107565', '159697146657862', '2144512926866', '160022669567832',
                               '159963315140718', '2236203632511', '0260493954680', '-', '353535', '2535993107804',
                               '0483912133576', '159876006163981', '159869458107565', ' ']  # 忽略的商品
        # 从barcodeList中去除ignore的商品
        for barcode in ignore_product_list:
            if barcode in barcodeList:
                barcodeList.remove(barcode)
        picTable = self.pos.LoadMatchProductsByPage()  # 获取所有在库商品的图片信息
        picDict = picTable['系统内图片'].astype(str).to_dict()  # 检查是否有图片的字典
        # print(picDict)
        for barcode in barcodeList:
            # 初始化行信息
            pRow = ori_df[ori_df['商品条码'].astype(str) == barcode].iloc[0]
            pName = pRow['商品名称']
            pCategory = pRow['商品分类']
            pPrice = pRow['商品原价']
            pStock = pRow['现有库存']
            pSaleCount = ori_df[ori_df['商品条码'].astype(str) == barcode]['销售数量'].sum()
            pAttention = ''
            row_content = [barcode, pName, pCategory, pPrice, pStock, pSaleCount, pAttention]

            # 名称规范检查
            if len(pName.split(' ')) < 2:
                row_content[-1] += '名称不规范！'

            # 检查是否有图片
            if picDict[str(barcode)] == '0.0':
                row_content[-1] += '没有图片！'

            # 检查库存是否错误
            if pStock != '-':
                if float(pStock) < 0:
                    row_content[-1] += '库存错误！'

            # 有关注事项的商品，添加到attention_df中
            if row_content[-1] != '':
                attention_df.loc[attention_df.shape[0]] = row_content

        attention_df = attention_df.sort_values('销量', ascending=False).reset_index(drop=True)
        # 如果需要生成markdown文件，那么就生成markdown文件,地址放在桌面/mmsdTables/
        if to_typora:
            with open('/Users/mengmeng/Desktop/萌萌书店相关/{} {} 日常商品排查表.md'.format(self.name, datetime.now().strftime(
                    "%Y-%m-%d %H:%M")), 'w') as f:
                f.write('## {}, {}'.format(self.name, datetime.today().strftime('%Y-%m-%d %H:%M')))
                f.write('\r\n')
                f.write('今日订单记录：{}条, 其中活跃sku数量： {}个, 其中需要关注的sku： {}个。'.format(
                    # ori_df 中 不同流水号的数量
                    ori_df['流水号'].unique().shape[0],
                    # 不同 barcode的数量
                    len(barcodeList),
                    # attention_df的数量
                    attention_df.shape[0]
                ))
                f.write('\r\n')

                f.write(attention_df.to_markdown())
                f.close()
        elif to_excel:
            attention_df.to_excel(
                excel_writer='## {}, {}'.format(self.name, datetime.today().strftime('%Y-%m-%d %H:%M')))
        elif to_html:
            attention_df.to_html(
                "/Users/mengmeng/Desktop/萌萌书店相关/{} {} 日常商品排查表.html".format(self.name, datetime.now().strftime(
                    "%Y-%m-%d %H:%M")))
        else:
            return print(attention_df)

    # 做一个函数，筛查僵尸商品
    def check_zombie(self):
        table = self.pos.LoadAdvancedProductsForBatchUpdate(createBeforeMonths=12, noSale=24)
        print(table.to_markdown())
        # for i in range(table.shape[0]):

    # 筛查库存积压产品
    def checkNoSale(self, month=3):
        table = self.pos.LoadAdvancedProductsForBatchUpdate(createBeforeMonths=3, noSale=month, stockRange=[10, 500])
        table.sort_values("库存", ascending=False, inplace=True)
        print(table.to_markdown())
        print(self.name, " 积压产品：")
        table = table[['商品名称', '条码', '规格', '库存', '商品分类', '修改日期']].reset_index(drop=True).astype(str)
        table.to_excel("{}积压产品.xlsx".format(self.name))
        # for i in range(table.shape[0]):
        #     barcode = table.loc[i, "条码"]
        #     table.loc[i,'最后销售时间'] =

    # 做一个函数，生成时间热力图
    def timeHeatMap(self, workDays=False, weekEnds=False):
        from matplotlib import pyplot as plt
        beginDate = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        table = self.pos.LoadProductSaleDetailsByPage(beginDateTime=beginDate)
        table['weekday'] = table["销售时间"].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').weekday())
        if workDays:
            table = table[table['weekday'] != 0]
            table = table[table['weekday'] != 6]
        if weekEnds:
            table = table[table['weekday'] != 1]
            table = table[table['weekday'] != 2]
            table = table[table['weekday'] != 3]
            table = table[table['weekday'] != 4]
            table = table[table['weekday'] != 5]

        table['hour'] = table['销售时间'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour)
        table = table.groupby('hour').sum('商品总价')
        # 在table中补齐hour列
        for i in range(24):
            if i not in table.index:
                table.loc[i] = 0
        # 画条形图
        plt.bar(table.index, table['商品总价'])
        plt.show()

    # 做一个函数，筛查商品进货的及时性
    def flow(self):
        productDf = self.pos.LoadProductsByPage(nums=10000).set_index('条码', drop=True)
        print(productDf)
        result_df = pd.DataFrame(columns=['日期', '条码', '品名', '进货数量', '进货以来的销量', '售出百分比'])
        df1 = self.pos.LoadProductStockFlowHistoryByPage()
        print(df1)
        df1 = df1[df1['入库门店'] == "萌萌书店(关天培店)"].reset_index(drop=True)
        print(df1)
        for i in range(df1.shape[0]):

            _date = df1.loc[i, '创建日期'].split(' ')[0]
            _barcode = df1.loc[i, '条码']
            _stockGet = df1.loc[i, '数量']
            _name = df1.loc[i, '商品名称']
            try:
                _stockNow = productDf.loc['{}'.format(_barcode), '库存']
            except:
                _stockNow = 0
            from mydb_fix import conn
            _summary = pd.read_sql(
                "select * from SaleRecords2 where productBarcode = '{}' and time > '{}'".format(_barcode, _date), conn)
            _saleCount = _summary['productQuantity'].sum()
            _wavePercent = int(round(float(_saleCount) / (float(_stockGet) + float(_stockNow)), 2) * 100)
            result_df.loc[i] = [_date, _barcode, _name, _stockGet, _saleCount, _wavePercent]
            # 在df1中删除这一行
            df1 = df1.drop(i)

        result_df[result_df['售出百分比'] > 50].sort_values('售出百分比', ascending=False).reset_index(drop=True).to_markdown(
            "优秀的采购！.md")
        result_df[result_df['售出百分比'] < 10].sort_values('售出百分比', ascending=True).reset_index(drop=True).to_markdown(
            "糟糕的采购！.md")

        # result_df[result_df['售出百分比'] < 10].to_markdown("不错的采购！")

    # 将活跃分类进行超类检查
    def check_active_category(self):
        catDict = self.pos.LoadCategoryDDLJson(to_dict=True)
        table = self.pos.LoadProductSaleDetailsByPage(beginDateTime='2022-04-01', endDateTime='2022-04-30', )

        # 筛选活跃分类
        categorysActive = table.groupby('商品分类').sum().sort_values('商品总价', ascending=False)
        # print(categorysActive.to_markdown())
        print("-" * 100)
        categorysList = categorysActive.index.to_list()
        categorysList.remove('无')

        # 输出表格格式
        resultDf = pd.DataFrame(columns=['销售额', '活跃sku', '总计sku', '活跃占比', '销售数量', '剩余库存', '库存波动', '库存成本', '库存总价'])
        # resultDf['商品分类'] = categorysList
        for category in categorysList:
            count = categorysActive.loc[category, '销售数量']
            amount = categorysActive.loc[category, '商品总价'].astype(str) + '元'
            activeSku = table[table['商品分类'] == category]['商品条码'].drop_duplicates().count()
            view = self.pos.summaryView(category=catDict["{}".format(category)], to_print=False)

            totalSku = self.pos.LoadProductsByPage(categoryJson=catDict["{}".format(category)])
            # 筛选出库存不为0的商品
            totalSku = totalSku[totalSku['库存'] != 0]
            totalSku = totalSku['条码'].drop_duplicates().count()
            activeRate = str(int(round(activeSku / totalSku, 4) * 100)) + '%'
            stock = float(view['stock'])
            buyPrice = str(int(float(view['buyPrice']))) + '元'
            sellPrice = str(int(float(view['sellPrice']))) + '元'
            try:
                wavePercent = str(int(round(float(count) / (float(stock) + float(count)), 4) * 100)) + '%'
            except:
                wavePercent = "error"
            resultDf.loc[category] = [amount, activeSku, totalSku, activeRate, count, stock, wavePercent, buyPrice,
                                      sellPrice]

        print(resultDf.to_markdown())

    # 查询今日活跃分类
    def get_active_category(self):
        table = self.pos.LoadProductSaleDetailsByPage().drop(
            ['Unnamed: 0', '商品原价', '商品折后价', '实收金额', '销售额占比', '成本', '利润'], axis=1)
        table = table.groupby(['商品分类']).sum().sort_values('商品总价', ascending=False)
        return table

    # 将银豹后台查询的方法，封装一个接口，pos
    @property
    def pos(self):
        from posFunctionsNew import PosPal
        return PosPal(self.user_id, self.phone)

    # 查询目前的分类情况，list[{'name':'', 'id':''},...]
    def query_category(self):
        session = get_zd_session()
        url = 'https://beta47.pospal.cn/Category/LoadCategorysWithOption'
        resp = session.post(url, data={'userId': '{}'.format(self.user_id), })
        cate_dic_list = resp.json()['categorys']
        cat_name_list = []
        for dic in cate_dic_list:
            cat_name_list.append(dic['name'])
        # print(cat_name_list)
        return cat_name_list

    # 生成该店铺下的全部ProCat
    @property
    def all_ProCat(self):
        from classProCat import ProCat
        dic = {}
        for cat in self.query_category():
            dic['{}'.format(cat)] = ProCat(name=cat, shopId=self.user_id, pos=self.pos)
        return dic

    # 检查商品是否销量上升
    def check_sales_up(self, barcode):
        Prod = self.Product(barcode)
        if Prod.get_tan(1) - Prod.get_tan(2) > Prod.get_tan(2) - Prod.get_tan(3):
            return True

    # 从数据表拉取今日销售商品的productBarcode列表
    def get_product_barcode_list(self):
        # 先获取今天的订单记录
        today = datetime.now().strftime('%Y-%m-%d')
        table = self.get_sale_records_by_dates(today)
        # 到数据表中拉取productBarcode列表
        product_barcode_list = table['productBarcode'].tolist()
        return product_barcode_list

    # 对某天的记录进行销量汇总
    def rank_day_table(self, date='', endDate=''):
        __table = self.get_sale_records_by_dates(date)
        print(__table)
        __table = __table.groupby(['productBarcode', 'productName'])['productQuantity'].sum().sort_values(
            ascending=False)
        print(__table[:5])

    # 从店铺生成一个商品对象
    def Product(self, barcode):
        # 如果传入的不是barcode，那么视为商品名称，需要先查询出来barcode
        if not barcode.isdigit():
            sql = '''
                SELECT productBarcode FROM SaleRecords2 WHERE productName = '{}'
            '''.format(barcode)
            try:
                barcode = conn.execute(sql).fetchone()[0]
            except:
                return print('条码转换错误，请检查商品名称是否正确')  # 如果查询不到，那么就返回
        from ClassProduct import Product
        return Product(barcode=barcode, Shop=self)

    # 根据商品名称或条码 查询数据库中的记录
    def query_by_name_or_barcode(self, name_or_barcode):
        sql = '''
        select * from SaleRecords2 where store = '{}' and (productBarcode = '{}' or productName = '{}')
        '''.format(self.name, name_or_barcode, name_or_barcode)
        df = pd.read_sql(sql, conn)
        return df

    # 根据范围查询SaleRecords2 的订单记录,
    def get_sale_records_by_dates(self, begin_or_by_date='', end_date=''):
        # 如果传入了2个日期，那么就按照指定的范围查询，如果只有一个日期，就按照那一天查询
        if begin_or_by_date != '' and end_date != '':
            start_date = begin_or_by_date
            end_date = end_date
        elif begin_or_by_date != '' and end_date == '':
            start_date = begin_or_by_date
            end_date = begin_or_by_date

        # 如果没有传入日期，默认为今天,beginDateTime为今天0点，endDateTime为今天24点
        elif begin_or_by_date == '' and end_date == '':
            # 如果当前时间小于8点，改为查询昨天的记录
            if datetime.now().hour < 8:
                start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                end_date = datetime.now().strftime('%Y-%m-%d')
            else:
                start_date = datetime.now().strftime('%Y-%m-%d')
                end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            print('参数错误')
            return

        start_date = start_date + ' 00:00:00'
        end_date = end_date + '23:59:59'

        # 查询订单记录
        sql = '''
        select * from SaleRecords2 where store = '{}' and time between '{}' and '{}'
        '''.format(self.name, start_date, end_date)
        df = pd.read_sql(sql, conn)
        return df

    # 根据范围查询saleRecords 的订单记录,范围是指从当前日期往前推recent_days天
    def get_sale_records_by_recent_days(self, recent_days=1):
        # 先获取今天的日期
        today = datetime.now().strftime('%Y-%m-%d')
        # 再获取今天的前recent_days天的日期
        start_date = (datetime.strptime(today, '%Y-%m-%d') - timedelta(days=recent_days)).strftime('%Y-%m-%d')
        # 用by_dates方法查询
        return self.get_sale_records_by_dates(start_date, today)

    # 获取今日销售业绩的说明 ，返回字典
    def get_performance(self, date=''):
        url = 'https://beta47.pospal.cn/Report/LoadBusinessSummaryV2'
        # 如果没有传入日期，默认为今天,beginDateTime为今天0点，endDateTime为今天24点
        if date == '':
            # 如果当前时间小于8点，那么就是昨天的业绩
            if datetime.now().hour < 8:
                date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            else:
                date = datetime.now().strftime('%Y-%m-%d')
            begin_date_time = date + ' 00:00:00'
            end_date_time = date + ' 23:59:59'
        # 如果指定的日期参数符合规则，就查询指定日期的业绩
        else:
            begin_date_time = date + ' 00:00:00'
            end_date_time = date + ' 23:59:59'
        # 定义一个字典，用来存储查询的参数
        params = {'userIds': '{}'.format(self.user_id), 'beginDateTime': begin_date_time,
                  'endDateTime': end_date_time}
        # 发送post请求，返回一个字典
        zd_session = get_zd_session()
        res = zd_session.post(url, params=params)
        # 将返回的字典中的'view'字段转换成BS4 BeautifulSoup对象
        soup = BeautifulSoup(res.json()['view'], 'html.parser')
        # print(soup)
        # 查找各指标的值，并去空格
        sale_amount = soup.find_all('tr')[1].find_all('td')[1].find('span').text
        cash_money = soup.find_all('tr')[11].find_all('td')[2].text.strip()
        union_pay_money = soup.find_all('tr')[11].find_all('td')[3].text.strip()
        recharge_money = soup.find_all('tr')[3].find_all('td')[1].find('span').text
        actual_money = soup.find_all('tr')[12].find_all('td')[1].find('span').text
        # 用字典保存查询的结果 并返回
        performance = {'sale_amount': sale_amount, 'cash_money': cash_money, 'union_pay_money': union_pay_money,
                       'recharge_money': recharge_money, 'actual_money': actual_money}
        return performance

    # 根据条码查询商品uid
    def get_product_id(self, barcode):
        """
        根据isbn，作为关键词查找后台商品id
        :param barcode:
        :return:
        """
        zd_session = get_zd_session()
        resp = zd_session.post(url='https://beta47.pospal.cn/Product/LoadProductsByPage', data={
            'groupBySpu': 'false',
            'userId': '{}'.format(self.user_id),
            'keyword': barcode,
            'enable': '1',
        })
        from lxml import etree
        _html = etree.HTML(resp.json()['contentView'])
        # print(_html.text)
        try:
            __id = _html.xpath('//tbody/tr[1]/@data')[0]
            return __id
        except:
            return print("查不到该商品")

    # 根据条码，到后台调用FindProduct
    def find_product(self, barcode):
        """
        根据isbn 获取商品后台信息
        :param barcode:
        :return: productjson
        """

        __id = self.get_product_id(barcode)
        zd_session = get_zd_session()
        _resp = zd_session.post(url='https://beta47.pospal.cn/Product/FindProduct', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0',
            # 'Content - Length': '20',
            'X-Requested-With': 'XMLHttpRequest'

        }, data={'productId': __id})
        return _resp

    # 检查是否有图片，从findproduct的结果中解析而来
    def check_image(self, barcode):
        """
        检查该商品是否有图片
        :param barcode:
        :return: bool 有t 无f
        """
        _dic = self.pos.FindProduct(barcode_or_name=barcode)
        return _dic['productimages'] == []


shop_list = [('萌萌书店(关天培店)', '18014151458', '4151410'), ('萌萌书店(山阳湖店)', '18014151459', '4455361')]
# 实例化2个商店
gtpShop = Shop(shop_list[0][0], shop_list[0][1], shop_list[0][2])
syhShop = Shop(shop_list[1][0], shop_list[1][1], shop_list[1][2])
