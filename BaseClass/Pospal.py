import json
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta

import requests


# 获取session
def get_session(numbers):
    url = 'https://beta47.pospal.cn/account/SignIn?noLog='
    headers = {
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/75.0.3770.100 Safari/537.36',
                  'Referer': 'https://beta47.pospal.cn',
                  'Connection': 'keep-alive',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                  'Upgrade-Insecure-Requests': '1',
              },
    data = {
        'userName': 'mmsd{}'.format(numbers),
        'password': 'francis003718',
        'returnUrl': '',
        'screenSize': '2560*1440'
    }
    temp_session = requests.session()
    temp_session.post(url, data=data)
    return temp_session  # 返回一个session   可以直接用于后续的请求


class PosPal(object):
    # 构造函数
    def __init__(self, userid, number):  # 初始化
        self.userid = userid  # 用户id
        self.zd_session = get_session('18014151457')  # 总店session
        self.session = get_session(number)  # 分店session

    # 设置秒杀商品
    def SaveSeckillRule(self):
        url = 'https://beta47.pospal.cn/EshopMarketing/SaveSeckillRule'

    # 获取商品设置for网店
    def FindProductWithOption(self, barcode):
        url = 'https://beta47.pospal.cn/Eshop/FindProductWithOption'
        data = {
            "userId": "{}".format(self.userid),
            "barcode": "{}".format(barcode)
        }
        resp = self.session.post(url, data)
        # 检查返回的数据是否正确
        if resp.json()['successed']:
            return resp.json()['product']
        else:
            print("请求错误，请检查barcode是否正确")
            return None

    # 保存网店商品修改
    def SaveProductWithOption(self, barcode, fixData={}):
        # 先获取商品信息
        findJson = self.FindProductWithOption(barcode=barcode)
        # 定义空的保存格式
        _saveJson = {'userId': '',  # 商店id
                     'productUid': '',  # 商品id
                     'eShopDisplayName': '',  # 商品在网店显示的名称 可不填
                     'buylimitPerDay': '',  # 每人每天限购数量 可不填
                     'eShopSellPrice': '',  # 商品在网店显示的价格 可不填
                     'newHideFromEShop': '',  # 是否在网店隐藏 1代表隐藏 0代表不隐藏
                     'hideOnEatIn': '',  # 是否堂食隐藏 1代表隐藏 0代表不隐藏
                     'hideOnTakeAway': '',  # 是否外卖隐藏 1代表隐藏 0代表不隐藏
                     'hideOnSelfTake': '',  # 是否自提隐藏 1代表隐藏 0代表不隐藏
                     'hideOnScanQRCode': '',  # 扫码点单隐藏 1代表隐藏 0代表不隐藏
                     'allowExpress': '',  # 是否允许快递 1代表允许 0代表不允许
                     'mappingBarcode': '',  # 商品条码 可不填
                     'enableVirtualStock': '',  # 是否启用虚拟库存 1代表启用 0代表不启用
                     'returnPolicy': '',  # 退货政策 可不填
                     'crossBorderProduct': '',  # 是否跨境商品 1代表是 0代表否
                     'virtualStock': '',  # 虚拟库存
                     }
        # 遍历保存格式中的key
        for att in _saveJson:
            # 判断需要保存的key，是否在已获取的商品信息中
            if att in findJson['productoption']:
                _saveJson[att] = findJson['productoption'][att]
            else:
                continue
        # 对fixData传入的参数进行修改
        if fixData:
            for key in fixData:
                if key in _saveJson:
                    _saveJson[key] = fixData[key]

        # 将保存数据生成完整传递json
        _data = {
            'productOptionJson': json.dumps(_saveJson, ensure_ascii=False),
            "groupBySpu": "", }
        print(_data)
        # 保存操作的url
        url = 'https://beta47.pospal.cn/Eshop/SaveProductOption'
        # 发送post
        r = self.session.post(url=url, data=_data)
        return r.content

    # 保存网店商品设置
    def SaveProductOption(self, barcode):
        url = 'https://beta47.pospal.cn/Eshop/SaveProductOption'
        data = {
            "productOptionJson": '{"userId":"4151410","productUid":"975385906959889216","eShopDisplayName":"",'
                                 '"buylimitPerDay":"","eShopSellPrice":"","newHideFromEShop":"0","hideOnEatIn":"1",'
                                 '"hideOnTakeAway":"1","hideOnSelfTake":"0","hideOnScanQRCode":"1","allowExpress":1,'
                                 '"mappingBarcode":"","enableVirtualStock":"0","returnPolicy":"",'
                                 '"crossBorderProduct":"0","virtualStock":0}',
            "groupBySpu": ""
        }
        resp = self.session.post(url, data)
        print(resp.text)

    # 获取网店商品列表
    def LoadEshopProductsByPage(self):
        url = 'https://beta47.pospal.cn/Eshop/LoadProductsByPage'
        data = {
            "groupBySpu": "",
            "userId": "4151410",
            "categorysJson": "[]",
            "enable": "1",
            "visible": "",
            "productTagUid": "",
            "keyword": "",
            "pageIndex": "1",
            "pageSize": "10000",
            "orderColumn": "",
            "asc": "true"
        }
        res = self.session.post(url, data=data)
        table = "<table>" + res.json()['contentView'] + "</table>"
        df = pd.read_html(table)[0].drop(columns=['Unnamed: 0', '编辑']).set_index('序号', drop=True)
        return df

    # 获取图片信息
    def LoadMatchProductsByPage(self, keyword='', withoutPic=False):
        url = 'https://beta47.pospal.cn/Eshop/LoadMatchProductsByPage'
        data = {
            "userId": self.userid,
            "categorysJson": "[]",
            "enable": "1",
            "pageIndex": "1",
            "pageSize": "10000",
            "asc": "false",
            "keyword": "{}".format(keyword)
        }
        resp = self.session.post(url, data)
        table = "<table>" + resp.json()['contentView'] + "</table>"
        table = table.replace('<img src="https://img.pospal.cn/productImages/0/default_200x200.png" />', '0')
        table = pd.read_html(table, index_col="商品条码")[0].drop(columns=['Unnamed: 0'])
        if withoutPic:
            return table[table['系统内图片'] == 0.0]
        return table

    # 调取货流单
    def LoadProductStockFlowHistoryByPage(self, days=30):  # days是要查询的最近天数
        url = 'https://beta47.pospal.cn/StockFlow/LoadProductStockFlowHistoryByPage'
        beginDateTime = (dt.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        endDateTime = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "userIds[]": "4151410",
            "beginTime": beginDateTime,
            "endTime": endDateTime,
            "pageIndex": "1",
            "pageSize": "10000",
            "asc": "false"
        }
        resp = self.session.post(url=url, data=data)
        return pd.read_html("<table>" + resp.json()['contentView'] + "</table>", index_col="Unnamed: 0")[0]

    # 高级商品筛查
    def LoadAdvancedProductsForBatchUpdate(self, categoryUid="", createBeforeMonths="", noSale=None,
                                           stockRange=[0, 0], brand=""):
        if createBeforeMonths != '':
            endDateTime = (dt.now() - timedelta(days=(float(createBeforeMonths) * 30))).strftime('%Y-%m-%d')
            endDateTime = str(endDateTime) + ' 23:59:59'
        else:
            endDateTime = str(dt.now().strftime('%Y-%m-%d %H:%M:%S'))
        beginDateTime = '2019-01-01' + ' 00:00:00'

        if not noSale:
            noSale = '6'

        url = 'https://beta47.pospal.cn/Product/LoadAddvancedProductsForBatchUpdate'
        data = {
            "queryString": "",
            "userId": self.userid,
            "categorysJson": "[{}]".format(categoryUid),
            "tagSelect": "",
            "createdDateRange[]": [
                beginDateTime,
                endDateTime
            ],
            'brandsJson': "[{}]".format(brand),
            "stockRange[]": stockRange,
            "noSale": noSale,
            "isProductRequestedStore": "false",
            "pageIndex": '1',
            "pageSize": '10000',

        }
        resp = self.session.post(url=url, data=data)
        return pd.read_html("<table>" + resp.json()['contentView'] + "</table>", index_col="Unnamed: 0")[0]

    # 加载商品分类的id json
    def LoadCategoryDDLJson(self, to_dict=False):
        url = 'https://beta47.pospal.cn/Category/LoadCategoryDDLJson'
        data = {'userId': self.userid}
        resp = self.session.post(url, data)
        df1 = pd.DataFrame(resp.json()['categorys']).set_index('name', drop=True)
        print(df1)
        if to_dict:
            return df1['uid'].to_dict()
        else:
            return df1

    # 获取销售记录，返回一个dataframe
    def LoadProductSaleDetailsByPage(self, keyword="", beginDateTime="", endDateTime="", ):
        url = 'https://beta47.pospal.cn/Report/LoadProductSaleDetailsByPage'
        if beginDateTime == '':
            if dt.now().hour < 8:
                beginDateTime = (dt.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            else:
                beginDateTime = dt.now().strftime('%Y-%m-%d')
            endDateTime = dt.now().strftime('%Y-%m-%d')

        beginDateTime = str(beginDateTime) + ' 00:00:00'
        endDateTime = str(endDateTime) + ' 23:59:59'

        data = {
            "keyword": "{}".format(keyword),
            "customerUid": "",
            "orderSource": "",
            "guiderUid": "",
            "beginDateTime": beginDateTime,
            "endDateTime": endDateTime,
            "brandUid": "",
            "supplierUid": "",
            "productTagUidsJson": "",
            "categorysJson": "[]",
            "brandUids": "[]",
            "pageIndex": "1",
            "pageSize": "10000",
            "orderColumn": "",
            "asc": "false"
        }
        resp = self.session.post(url, data=data)  # 请求服务器
        table = resp.json()['contentView']  # 解析返回的json数据
        table = "<table>" + table + "</table>"  # 对内容修饰table标签
        table = pd.read_html(table, index_col="Unnamed: 0")[0]  # pandas读取table
        return table

    # 获取销售记录，返回一个dataframe
    def LoadProductSaleDetailsSummary(self, keyword="", customerUid="", orderSource="", beginDateTime="",
                                      endDateTime="", pageIndex=1, pageSize=10000, brandUid="", ):
        url = 'https://beta47.pospal.cn/Report/LoadProductSaleDetailsSummary'
        if beginDateTime == '':
            if dt.now().hour < 8:
                beginDateTime = (dt.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            else:
                beginDateTime = dt.now().strftime('%Y-%m-%d')
            endDateTime = dt.now().strftime('%Y-%m-%d')

        beginDateTime = str(beginDateTime) + ' 00:00:00'
        endDateTime = str(endDateTime) + ' 23:59:59'

        data = {
            "keyword": "{}".format(keyword),
            "customerUid": "",
            "orderSource": "",
            "guiderUid": "",
            "beginDateTime": beginDateTime,
            "endDateTime": endDateTime,
            "brandUid": "",
            "supplierUid": "",
            "productTagUidsJson": "",
            "categorysJson": "[]",
            "brandUids": "[]",
            "pageIndex": "1",
            "pageSize": "10000",
            "orderColumn": "",
            "asc": "false"
        }
        resp = self.session.post(url, data=data)
        # table = resp.json()['contentView']
        # table = "<table>" + table + "</table>"
        # table = pd.read_html(table)[0]
        # print(resp.content)
        return resp.json()['summaryView']

    # 根据条码查询id
    def get_pid(self, keyword='', ):
        url = 'https://beta47.pospal.cn/Product/LoadProductsByPage'
        data = {'groupBySpu': 'False',
                'userId': self.userid,
                'pageSize': "100",
                'pageIndex': 1,
                'enable': "1",
                'asc': 'false',
                'keyword': keyword,
                'categorysJson': "[]",
                'supplierUid': "[]",
                'orderColumn': '',
                'productTagUidsJson': '[]',
                }
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.142 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',

        }
        response = self.session.post(url, data=data, headers=headers)
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'lxml')
            pid = soup.find_all('tr')[1]['data']
            pid = pid[2:-2]
            return pid
        except:
            print('查询商品id失败')

    # 根据分类查询loadProductsByPage，返回list[dict]
    def LoadCategorysWithOption(self):
        # Loads categorys from url
        # Returns a list of categorys
        url = 'https://beta47.pospal.cn/Category/LoadCategorysWithOption'
        data = {
            "userId": "{}".format(self.userid),
        }
        resp = self.session.post(url, data)
        return resp.json()['categorys']

    # 获取商品信息方法：
    def LoadProductsByPage(self, nums=100, groupBySpu='False', enable="1", asc='False', keyword='',
                           categoryJson='', supplierUid="[]"):
        url = 'https://beta47.pospal.cn/Product/LoadProductsByPage'
        data = {'groupBySpu': groupBySpu,
                'userId': self.userid,
                'pageSize': nums,
                'pageIndex': 1,
                'enable': enable,
                'asc': asc,
                'keyword': keyword,
                'categorysJson': "[{}]".format(categoryJson),
                'supplierUid': supplierUid,
                'orderColumn': '',
                'productTagUidsJson': '[]',
                }
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.142 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',

        }
        response = self.session.post(url, data=data, headers=headers)
        table = response.json()['contentView']
        table = '<table>' + table + '</table>'
        df = pd.read_html(table)[0]
        return df

    # 获取商品概览：
    def LoadProductSummary(self, keyword='', category='', supplierUid='[]'):
        url = 'https://beta47.pospal.cn/Product/LoadProductSummary'
        data = {
            'groupBySpu': 'false',
            'userId': self.userid,
            'productbrand': '',
            'categorysJson': '["{}",]'.format(category),
            'enable': '1',
            'supplierUid': '',
            'productTagUidsJson': '[{}]'.format(supplierUid),
            'keyword': "{}".format(keyword),
            'categoryType': '',
        }
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',

        }
        response = self.session.post(url, data=data, headers=headers)
        return response

    # 概览summary
    def summaryView(self, keyword='', category='', supplierUid='', to_print=False, ):
        resp = self.LoadProductSummary(keyword=keyword, category=category, supplierUid=supplierUid)
        text = resp.json()['summaryView'].split('，')
        skus = text[0].split(' ')[1]
        stocks = text[1].split('：')[1]
        buyPrices = text[2].split('：')[1]
        sellPrices = text[3].split('：')[1].split('<')[0]
        __result = {
            'total': skus,
            'stock': stocks,
            'buyPrice': buyPrices,
            'sellPrice': sellPrices
        }
        if to_print:
            print(__result)
            return __result
        else:
            return __result

    # 获取单个商品的详细信息：
    def FindProduct(self, barcode_or_name=None, productId=None, ):
        if productId:
            __id = productId
        elif barcode_or_name:
            __id = self.get_pid(keyword=barcode_or_name)
        else:
            print('请输入商品名称或者条形码')
            return
        # 开始查询商品详细信息：
        url = 'https://beta47.pospal.cn/Product/FindProduct'
        data = {
            'productId': __id,
        }
        response = self.session.post(url, data=data)
        return response.json()['product']

    # 保存商品： 暂时不可用
    def SaveProduct(self, barcode=None, fixData={}, ):
        findJson = self.FindProduct(barcode_or_name=barcode)
        saveJson = {
            "id": "",
            "enable": "",
            "userId": "",
            "barcode": "",
            "name": "",
            "categoryUid": "",
            "categoryName": "",
            "sellPrice": "",
            "buyPrice": "",
            "isCustomerDiscount": "",
            "customerPrice": "",
            "sellPrice2": "",
            "pinyin": "",
            "supplierUid": "",
            "supplierName": "",
            "supplierRangeList": "",
            "productionDate": "",
            "shelfLife": "",
            "maxStock": "",
            "minStock": "",
            "description": "",
            "noStock": "",
            "stock": "",
            "attribute6": "",
            "attribute9": "",
            "productCommonAttribute": "",
            "baseUnitName": "",
            "customerPrices": "",
            "productUnitExchangeList": "",
            "attribute1": "",
            "attribute2": "",
            "attribute3": "",
            "attribute4": "",
            "productTags": ""
        }
        for att in saveJson:
            if att in findJson:
                saveJson[att] = findJson[att]

        url = 'https://beta47.pospal.cn/Product/SaveProduct'
        if fixData:
            for key in fixData:
                if key in saveJson:
                    saveJson[key] = fixData[key]
                    data = {'productJson': json.dumps(saveJson)}
                    response = self.session.post(url, data=data, )
                    return print(response.content)
                else:
                    print('{} 字段不存在，请检查'.format(key))
                    return None
        else:
            print("没有修改内容，在fixData{}中添加修改内容")
            return None
