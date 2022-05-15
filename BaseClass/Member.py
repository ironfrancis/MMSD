import json

import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime as dt
from datetime import timedelta

from BaseClass.myDatabase import conn


class Member(object):
    # 初始化 会员实例，需要姓名和手机号
    def __init__(self, name, number):
        self.name = name
        self.number = number

    # 会员历史消费记录
    @property
    def history(self):
        _df = pd.read_sql("SELECT * FROM SaleRecords WHERE 会员卡号 = '{}'".format(self.number), conn)
        return _df

    def info(self):
        _df = self.history
        __latest = _df.sort_values(by='销售时间', ascending=False).iloc[0]['销售时间']
        __oldest = _df.sort_values(by='销售时间', ascending=True).iloc[0]['销售时间']
        __latest, __oldest = dt.strptime(__latest, "%Y-%m-%d %H:%M:%S"), dt.strptime(__oldest, "%Y-%m-%d %H:%M:%S")
        memberInfo = dictdateRange = (__latest - __oldest).days
        dateRange = (__latest - __oldest).days
        ids = _df['流水号'].drop_duplicates().shape[0]
        _sequence = round(ids / dateRange, 2)
        intervalDaysAvg = round(dateRange / ids, 2)
        sinceLast = (dt.now() - __latest).days
        categorys = _df['商品分类'].drop_duplicates().shape[0]
        cateList = _df.groupby('商品分类').sum()['商品总价'].sort_values(ascending=False).head(5).index.tolist()
        maxPrice = _df['商品原价'].max()
        minPrice = _df['商品原价'].min()
        avgPrice = round(_df['商品原价'].mean(), 2)

        memberInfo = dict(
            会员姓名=self.name,
            会员卡号=self.number,
            初次消费日期=__oldest.strftime("%Y-%m-%d"),
            最近消费日期=__latest.strftime("%Y-%m-%d"),
            消费时间范围=memberInfo,
            消费次数=ids,
            日均消费次数=_sequence,
            平均消费间隔=intervalDaysAvg,
            距离最近消费=sinceLast,
            商品分类数=categorys,
            喜爱的分类前五=cateList,
            最高单品金额=maxPrice,
            最低单品金额=minPrice,
            平均单品金额=avgPrice
        )

        return json.dumps(memberInfo, ensure_ascii=False, indent=8)


mb = Member('李梓德', '17368110918')
print(mb.info())
print("ok")
