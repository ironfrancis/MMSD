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
_saveJson = {'userId': '', 'productUid': '', 'eShopDisplayName': '', 'buylimitPerDay': '', 'eShopSellPrice': '',
             'newHideFromEShop': '', 'hideOnEatIn': '', 'hideOnTakeAway': '', 'hideOnSelfTake': '',
             'hideOnScanQRCode': '', 'allowExpress': '', 'mappingBarcode': '', 'enableVirtualStock': '',
             'returnPolicy': '', 'crossBorderProduct': '', 'virtualStock': ''}
print("findJson", json.dumps(findJson, indent=5, ensure_ascii=False))
for att in _saveJson:
    if att in findJson:
        print("检索字段", att, "检索结果", findJson[att])
        _saveJson[att] = findJson[att]
    else:
        continue
print("-------------------------------")
print("saveJson", json.dumps(_saveJson, indent=5, ensure_ascii=False))
