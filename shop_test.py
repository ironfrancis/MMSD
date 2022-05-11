import json

from BaseClass.Shop import gtpShop

# gtpShop.eshopList()


# print(gtpShop.find_product(6973830380878))
catinfo = gtpShop.query_category(to_json=True,type=1)
# resultDict = {}
# for c in catinfo:
#     if c['parentUid'] == 0:
#         # print(c)
#         resultDict[c['name']] = c['uid']
#
# print(json.dumps(resultDict,ensure_ascii=False,indent=5))
print(catinfo)

