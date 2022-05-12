import json

import BaseClass.Shop

text = {
    "productOptionJson": "{\"userId\":\"4151410\",\"productUid\":\"1073691224840181963\",\"eShopDisplayName\":\"\","
                         "\"buylimitPerDay\":\"\",\"eShopSellPrice\":\"\",\"newHideFromEShop\":\"1\","
                         "\"hideOnEatIn\":\"0\",\"hideOnTakeAway\":\"0\",\"hideOnSelfTake\":\"0\","
                         "\"hideOnScanQRCode\":\"0\",\"allowExpress\":1,\"mappingBarcode\":\"\","
                         "\"enableVirtualStock\":\"0\",\"returnPolicy\":\"\",\"crossBorderProduct\":\"0\","
                         "\"virtualStock\":0}",
    "groupBySpu": ""
}

pOptionJson = json.loads(json.loads(json.dumps(text, indent=5, ensure_ascii=False))['productOptionJson'])

findJson = BaseClass.Shop.gtpShop.pos.FindProductWithOption(barcode='00223393')
_saveJson = {'userId': '',          # 商店id
             'productUid': '',      # 商品id
             'eShopDisplayName': '',    # 商品在网店显示的名称 可不填
             'buylimitPerDay': '',      # 每人每天限购数量 可不填
             'eShopSellPrice': '',       # 商品在网店显示的价格 可不填
             'newHideFromEShop': '',    # 是否在网店隐藏 1代表隐藏 0代表不隐藏
             'hideOnEatIn': '',         # 是否堂食隐藏 1代表隐藏 0代表不隐藏
             'hideOnTakeAway': '',      # 是否外卖隐藏 1代表隐藏 0代表不隐藏
             'hideOnSelfTake': '',      # 是否自提隐藏 1代表隐藏 0代表不隐藏
             'hideOnScanQRCode': '',    # 扫码点单隐藏 1代表隐藏 0代表不隐藏
             'allowExpress': '',        # 是否允许快递 1代表允许 0代表不允许
             'mappingBarcode': '',      # 商品条码 可不填
             'enableVirtualStock': '',  # 是否启用虚拟库存 1代表启用 0代表不启用
             'returnPolicy': '',        # 退货政策 可不填
             'crossBorderProduct': '',  # 是否跨境商品 1代表是 0代表否
             'virtualStock': '',         # 虚拟库存
             }
print("findJson", json.dumps(findJson, indent=5, ensure_ascii=False))
g = 0
for att in _saveJson:
    if att in findJson['productoption']:
        print("检索字段", att, "检索结果", findJson['productoption'][att])
        _saveJson[att] = findJson['productoption'][att]
        g += 1
    else:
        print(att,"没有在findJson中找到")
        continue
print("-------------------------------")
print("saveJson", json.dumps(_saveJson, indent=5, ensure_ascii=False))
print("saveJson 共有字段数量", len(_saveJson) ,"can get in Find Json",g)

r = BaseClass.Shop.gtpShop.pos.session.post(
    url = 'https://beta47.pospal.cn/Eshop/SaveProductOption',
    data={
        'productOptionJson': json.dumps(_saveJson, ensure_ascii=False),
        "groupBySpu": "",
    })
print("-------------------------------")
print("r.text", r.text)