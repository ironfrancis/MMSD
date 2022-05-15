import json

import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime as dt
from datetime import timedelta

import BaseClass.Pospal
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
        _df2 = pd.read_sql("SELECT * FROM RechargeRecords WHERE 会员手机号 = '{}'".format(self.number), conn)
        return _df, _df2

    def info(self):
        _sale_df, _recharge_df = self.history
        # print(_sale_df.to_markdown())
        __latest = _sale_df.sort_values(by='销售时间', ascending=False).iloc[0]['销售时间']
        __oldest = _sale_df.sort_values(by='销售时间', ascending=True).iloc[0]['销售时间']
        __latest, __oldest = dt.strptime(__latest, "%Y-%m-%d %H:%M:%S"), dt.strptime(__oldest, "%Y-%m-%d %H:%M:%S")
        dateRange = (__latest - __oldest).days
        ids = _sale_df['流水号'].drop_duplicates().shape[0]
        _sequence = round(ids / dateRange, 2)
        intervalDaysAvg = round(dateRange / ids, 2)
        sinceLast = (dt.now() - __latest).days
        categorys = _sale_df['商品分类'].drop_duplicates().shape[0]
        cateList = _sale_df.groupby('商品分类').sum()['商品总价'].sort_values(ascending=False).head(5).index.tolist()
        maxPrice = _sale_df['商品原价'].max()
        minPrice = _sale_df['商品原价'].min()
        avgPrice = round(_sale_df['商品原价'].mean(), 2)
        # 时间分布,汇总星期一到星期五的的销售量和销售额，周末的销售量和销售额
        _sale_df['星期'] = _sale_df['销售时间'].apply(lambda x: dt.strptime(x, "%Y-%m-%d %H:%M:%S").weekday())
        _sale_df['日期'] = _sale_df['销售时间'].apply(lambda x: dt.strptime(x, "%Y-%m-%d %H:%M:%S").date())
        _weekday = {
            "最常访问": "星期" + str(_sale_df['星期'].value_counts(ascending=False).index[0] + 1),
        }
        for iw in range(0, 7):
            _weekday["星期" + str(iw + 1)] = dict(
                消费次数=_sale_df[_sale_df['星期'] == iw].shape[0],
                次数占比=round(_sale_df[_sale_df['星期'] == iw].shape[0] / _sale_df.shape[0] * 100, 0),
                消费金额=_sale_df[_sale_df['星期'] == iw]['商品总价'].sum(),
                金额占比=round(_sale_df[_sale_df['星期'] == iw]['商品总价'].sum() / _sale_df['商品总价'].sum() * 100, 0), )

        memberInfo = dict(
            会员姓名=self.name,
            会员卡号=self.number,
            常用店铺=_sale_df['销售门店'].drop_duplicates().to_string(index=False),
            累计充值=_recharge_df['充值金额'].sum(),
            初次消费日期=__oldest.strftime("%Y-%m-%d"),
            最近消费日期=__latest.strftime("%Y-%m-%d"),
            会籍天数=dateRange,
            活跃天数=_sale_df['日期'].unique().shape[0],
            消费次数=ids,
            日均消费次数=_sequence,
            平均消费间隔=intervalDaysAvg,
            距离最近消费=sinceLast,
            星期分布=_weekday,
            商品分类数=categorys,
            喜爱的分类前五=str(cateList),
            消费总金额=_sale_df['商品总价'].sum(),
            最高单品金额=maxPrice,
            最低单品金额=minPrice,
            平均单品金额=avgPrice,
        )
        # 根据活跃天数会籍天数 计算概率1
        memberInfo['访问概率'] = round(memberInfo['活跃天数'] / memberInfo['会籍天数'] * 100, 2)

        # 根据 星期分布 进行修正1
        memberInfo['访问概率'] = memberInfo['访问概率'] / (100 / 7) * memberInfo['星期分布'][('星期' + str(dt.now().weekday() + 1))][
            '次数占比']

        # 根据日均消费次数 进行修正2

        return memberInfo


def all_mb():
    zd_session = BaseClass.Pospal.get_session(numbers='18014151457')
    url = 'https://beta47.pospal.cn/Customer/LoadCustomersByPage'
    data = {
        "createUserId": "[4151410,4455361]",
        "categoryUid": "",
        "tagUid": "",
        "type": "1",
        "guiderUid": "",
        "keyword": "",
        "pageIndex": "1",
        "pageSize": "10000",
        "orderColumn": "",
        "asc": "false"
    }
    df1 = pd.read_html("<table>" + zd_session.post(url, data=data).json()['contentView'] + "</table>",
                       index_col='Unnamed: 0')[0]
    df1 = df1[df1['余额'] > 0].reset_index(drop=True)
    print(df1)
    __mbList = []
    for i in range(0, df1.shape[0]):
        __mbList.append(Member(df1.loc[i, '姓名'], df1.loc[i, '会员号']))
    return __mbList


# mblist = [
#     Member('李梓德', '17368110918'),
#     Member('徐千树', '13511531126'),
#     Member('王米珂', '15240261190'),
#     Member('西西妈', '13382307377'),
#     Member('葛洪凤', '160413182929'),
# ]
df2 = pd.DataFrame(columns=['name', 'rou'])
for mb in all_mb():
    try:
        df2.loc[df2.shape[0]] = [mb.name, mb.info()['访问概率']]
    except:
        continue

print(df2.sort_values(by='rou', ascending=False).head(50))
