---

---

# MMSD System V0.2 introduction
## Shop

门店操作的类

Class Shop

Gtpd = Shop(name, phone, user_id)

- name：店名
- phone：电话
- User_id：银豹系统对应的商店userid

### 类方法列表：

| 函数名                                                       | 作用                                          | 备注                                          |
| ------------------------------------------------------------ | --------------------------------------------- | --------------------------------------------- |
| Database                                                     | 数据库实例                                    | 属性                                          |
| Cat(self,name)                                               | 超类实例                                      |                                               |
| check_zombie()                                               | 针对门店，查询僵尸商品                        | 返回df                                        |
| checkNoSale(self, month=3)                                   | 查询积压商品                                  | 返回df                                        |
| timeHeatMap(self, workDays=False, weekEnds=False)            | 销售热力图（小时）                            | 返回plt.Bar                                   |
| flow(self)                                                   | 进货分析                                      | 返回df                                        |
| check_active_category(self)                                  | 对活跃分类进行分析                            | 返回df                                        |
| get_active_category(self)                                    | 日活分类统计                                  | 返回df                                        |
| pos                                                          | 银豹操作接口                                  |                                               |
| query_category(self)                                         | 查询目前的分类情况                            | 返回字典                                      |
| all_ProCat                                                   | 生成全部超类                                  | 返回dict{分类名：超类对象，类名：超类对象...} |
| check_sales_up(self, barcode)                                | 根据条码查询商品是否处于销量上升中            | 返回布尔值                                    |
| get_product_barcode_list(self)                               | 日活sku的条码列表                             | 返回list                                      |
| rank_day_table(self, date='', endDate='')                    | 日销售记录统计                                | 返回df                                        |
| Product(self, barcode)                                       | 从店铺生成一个商品对象，内含商品操作接口      | 返回一个Product对象                           |
| query_by_name_or_barcode(self, name_or_barcode)              | 从本地数据库读取某商品的全部记录              | 返回df                                        |
| productDailyCheck()                                          | 生成店铺每日商品检查表的                      | to_typora生成md文件                           |
| get_sale_records_by_dates(self, begin_or_by_date='', end_date='') | 从数据库查询销售记录                          | 返回df                                        |
| def get_sale_records_by_recent_days(self, recent_days=1)     | 根据最近日期，查询本地数据库记录              | 返回df                                        |
| get_performance(self, date='')                               | 银豹后台查询业绩概览                          | 返回字典                                      |
| get_product_id(self, barcode)                                | 根据条码查询uid                               | 返回str                                       |
| find_product(self, barcode)                                  | 根据条码，调用findproduct                     | 返回 响应resp                                 |
| check_image(self, barcode)                                   | 检查是否有图片，从findproduct的结果中解析而来 | True False                                    |
|                                                              |                                               |                                               |



### 功能接口

| 形式                  | 说明                                   | 包地址               |
| --------------------- | -------------------------------------- | -------------------- |
| shop.pos              | 转属性，无需传参，生成银豹操作实例对象 | posFunctionsNew.py   |
| shop.Cat(name)        | 以name为名称的超类ProCat对象           | classProCat.py       |
| shop.Product(barcode) | 以barcode为条码的商品对象              | ClassProduct.py      |
| shop.DataBase         | 转属性，无参数，返回数据库功能接口     | baseClass/classDb.py |



### 商品信息维护表

```python
shop.productDailyCheck()
```

| 参数            | 作用          |
| --------------- | ------------- |
| to_typora=False | 生成md文件    |
| to_excel=False  | 生成excel文件 |

1. pos接口获取当日销售流水记录 存在ori_df

2. 筛选ori_df中的条码列表，视作日活sku，存为barcoderList

3. pos接口统一获取商品图片库信息，将没有修改的原始默认图替换为0.0字段，保存在picDict中

4. 初始化空的结果表格columns=['条码', '商品名称', '分类', '售价', '库存', '销量', '关注事项：']

5. 遍历barcodeList

   ```python
   # 初始化行信息
   pName = ori_df[ori_df['商品条码'] == barcode]['商品名称'].values[0]
   pCategory = ori_df[ori_df['商品条码'] == barcode]['商品分类'].values[0]
   pPrice = ori_df[ori_df['商品条码'] == barcode]['商品原价'].values[0]
   pStock = ori_df[ori_df['商品条码'] == barcode]['现有库存'].astype(float).values[0]
   pSaleCount = ori_df[ori_df['商品条码'] == barcode]['销售数量'].sum()
   pAttention = ''
   row_content = [barcode,pName,pCategory,pPrice,pStock,pSaleCount,pAttention]
   ```

6. 根据规则进行筛查

   ```python
   # 名称规范检查
   if len(pName.split(' ')) < 2:
       row_content[-1] += '名称不规范！'
   
   # 检查是否有图片
   if picDict[barcode] == 0:
       row_content[-1] += '没有图片！'
   
   # 检查库存是否错误
   if pStock < 0:
       row_content[-1] += '库存错误！'
   ```





------

## PosPal 银豹服务器接口



### PosPal类

```python
    # 构造函数
    def __init__(self, userid, number):                         # 初始化
        self.userid = userid                                    # 用户id
        self.zd_session = get_session('18014151457')            # 总店session
        self.session = get_session(number)                      # 分店session
```



### LoadProductStockFlowHistoryByPage  调取货流记录

```python
# 调取货流单
def LoadProductStockFlowHistoryByPage(self,days=30):						# days是要查询的最近天数
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
    return pd.read_html("<table>" + resp.json()['contentView'] + "</table>",index_col="Unnamed: 0")[0]
```

参数days默认30，代表查询最近30天以来的出入库记录。



### LoadAddvancedProductsForBatchUpdate 高级商品筛选

```python
    # 高级商品筛查
    def LoadAddvancedProductsForBatchUpdate(self, categoryUid="", createBeforeMonths="", noSale=None,stockRange=[0,0],):
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
            "stockRange[]": stockRange,
            "noSale": noSale,
            "isProductRequestedStore": "false",
            "pageIndex": '1',
            "pageSize": '10000',

        }
        resp = self.session.post(url=url, data=data)
        return pd.read_html("<table>" + resp.json()['contentView'] + "</table>",index_col="Unnamed: 0")[0]
```



### LoadCategoryDDLJson 获取商品分类信息

```python
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
```



### LoadProductSaleDetailsByPage 销售流水记录

```python
    # 获取销售记录，返回一个dataframe
    def LoadProductSaleDetailsByPage(self, keyword="", beginDateTime="",endDateTime="", ):
        url = 'https://beta47.pospal.cn/Report/LoadProductSaleDetailsByPage'
        if beginDateTime == '':					# 如果未传入时间参数，默认为今天
            if dt.now().hour < 8:				# 如果当前时间早于上午8点，则查询昨天的数据
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
        resp = self.session.post(url, data=data)            # 请求服务器
        table = resp.json()['contentView']                  # 解析返回的json数据
        table = "<table>" + table + "</table>"              # 对内容修饰table标签
        table = pd.read_html(table)[0]                      # pandas读取table
        return table
```



### LoadProductsByPage 搜索商品页

```python
# 获取商品信息方法：
def LoadProductsByPage(self, nums=100, groupBySpu='False', enable="1", asc='False', keyword='',
                       categoryJson='', supplierUid="[]"):
    url = 'https://beta47.pospal.cn/Product/LoadProductsByPage'
    data = {'groupBySpu': groupBySpu,
            'userId': self.userid,
            'pageSize': nums,
            'pageIndex': 1,
            'enable': enable,
            'asc': 'false',
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
```



### LoadProductSummary 获取商品概览

```python
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
```



### summaryView 商品页汇总概览

```python
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
```



### FindProduct 商品详细信息获取

参数为商品的条形码、名称，则以名称或条码为keyword搜索银豹后台，得到最佳匹配到的商品的id，或直接传入id到银豹后台进行查询。这里返回响应json中的product字段下的内容。

```python
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
```



### LoadMatchProductsByPage 检查图片

对应后台功能——商品图片库，根据返回值中的图片地址是否为默认地址，判断是否有上传图片，返回在库所有商品的图片信息df，没有照片的记录【系统内图片】字段标记为0.0 （float）

```python
# 获取图片信息
def LoadMatchProductsByPage(self):
    url = 'https://beta47.pospal.cn/Eshop/LoadMatchProductsByPage'
    data = {
        "userId": self.userid,
        "categorysJson": "[]",
        "enable": "1",
        "pageIndex": "1",
        "pageSize": "10000",
        "asc": "false"
    }
    resp = self.session.post(url, data)
    table = "<table>" + resp.json()['contentView'] + "</table>"
    table = table.replace('<img src="https://img.pospal.cn/productImages/0/default_200x200.png" />','0')
    return pd.read_html(table, index_col="商品条码")[0].drop(columns=['Unnamed: 0'])
```



------

## DataBase 数据库接口



### class DataBase 实例构造

```python
    def __init__(self, shop_id, shop_name):
        self.conn = sqlite3.connect(dbpath)   # 创建数据库连接
        self.cursor = self.conn.cursor()      # 创建游标
        self.shop_id = shop_id                # 指定店铺id
        self.shop_name = shop_name            # 指定店铺名
```



### query_last_sale_time 最近销售时间

```python
# 做一个查询最近销售时间的操作,根据shop_name和barcode
def query_last_sale_time(self, barcode):
    sql = "select time from SaleRecords2 where store = '%s' and productBarcode = '%s'" % (self.shop_name, barcode)
    self.cursor.execute(sql)
    result = self.cursor.fetchone()
    return result
```

返回一个日期字段。





## ProCat 超类接口









## WebApi 第三方接口



### Deli 得力

#### brandPicFix()

根据keyword=得力 查询商品库，并获取图片，保存本地



### MG 晨光

#### mgBarcodeScan（barcode）

根据条形码查询晨光联盟app，返回json



#### mgGetImage（barcode）

根据条形码查询晨光联盟商品，从返回中得到商品内部id，在使用get方法，http://lifemg.cn/v4/h5/item/itemId，获取商品图片

------

## Sqlite3 数据库

