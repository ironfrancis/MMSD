import json

import pandas as pd
import xlrd

from BaseClass.Shop import gtpShop

# gtpShop.eshopList()


# print(gtpShop.find_product(6973830380878))
# catinfo = gtpShop.query_category(to_json=True,type=1)
# resultDict = {}
# for c in catinfo:
#     if c['parentUid'] == 0:
#         # print(c)
#         resultDict[c['name']] = c['uid']
#
# print(json.dumps(resultDict,ensure_ascii=False,indent=5))
# print(catinfo)
# for c in catinfo.items():
#     catId = c[1]
#     catName = c[0]
#     table = gtpShop.pos.LoadProductsByPage(categoryJson=catId)
#     print(catName)
#     print(table)

gtpShop.pos.SaveProduct(barcode=6941025155914, )
