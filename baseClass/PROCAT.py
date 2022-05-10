import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime as dt, timedelta


# 定义一个类，用于操作超级分类（ProCat）
class ProCat(object):
    def __init__(self, name, shopId=None, pos=None):
        self.name = name
        self.shop_id = shopId
        self.pos = pos

    # 根据分类名，查询uid
    @property
    def uid(self):
        uidDict = self.pos.LoadCategoryDDLJson(to_dict=True)
        return uidDict[self.name]

    # 银豹后台分类商品查询，返回df
    @property
    def loadProducts(self):
        df = self.pos.LoadProductsByPage(nums=1000,categoryJson=self.uid)
        return df

    @property
    def skus(self):
        df = self.loadProducts
        skus = df.shape[0]
        return skus

    @property
    def sum_stocks(self):
        df = self.loadProducts
        # 删除库存为'-'的商品
        df = df[df['库存'] != '-']
        sum_stocks = df['库存'].astype(float).sum()
        return sum_stocks

    @property
    def avg_stock(self):
        df = self.loadProducts
        avg_stock = df['库存'].mean()
        return avg_stock

    @property
    def max_stock(self):
        # 拥有最大库存的商品是哪个？
        df = self.loadProducts
        max_stock = df['库存'].max()
        return max_stock

    @property
    def mid_stock(self):
        # 库存的中位数
        df = self.loadProducts
        mid_stock = df['库存'].median()
        return mid_stock

    @property
    def all_amount(self):
        # 计算所有商品的总销售额
        df = self.loadProducts
        # 计算每条商品的销售价乘以库存
        df['amount'] = df['销售价'] * df['stock']
        # 求和
        all_amount = df['amount'].sum()
        return all_amount

    @property
    def avg_price(self):
        # 计算平均价格
        return round(self.all_amount / self.sum_stocks, 2)

    @property
    def mid_price(self):
        # 计算价格中位数
        df = self.loadProducts
        mid_price = df['销售价'].median()
        return mid_price

    # 做一个画直方图函数
    def draw_bar(self, to_file=False, attention=False):
        plt.rcParams['font.sans-serif'] = ['Songti SC']
        plt.rcParams['font.size'] = 14
        df = self.loadProducts
        # 按照销售价合并库存
        df2 = df[['商品名称', '销售价', '库存']]
        df2 = df2[df2['库存'] != 0]
        df2.reset_index(drop=False, inplace=True)
        df2 = df2.groupby(['销售价']).sum('库存')
        # 调用hist画图
        plt.style.use('ggplot')
        try:
            df2.sort_values('销售价').plot(kind='bar', y='库存', )
        except TypeError:
            return print('绘图错误，请检查数据')
        plt.xlabel('销售价')
        plt.ylabel('库存')
        plt.title('{} 分类下，sku：{} , 总库存 {}'.format(self.name, self.skus, self.sum_stocks))
        if to_file:
            plt.savefig('ProCat/{}/{}.png'.format(self.shop_id, self.name))
            return
        else:
            plt.show()
            return None

