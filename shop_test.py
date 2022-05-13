import json
import pandas as pd

from BaseClass.Shop import gtpShop

# print(gtpShop.pos.LoadProductSaleDetailsByPage())
mblist = gtpShop.pos.LoadProductSaleDetailsByPage()['会员卡号'].unique()
for mb in mblist:
    print(mb)
    # print(gtpShop.pos.LoadProductSaleDetailsByPage(mb))
    print("-" * 50)
