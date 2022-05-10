from baseClass.Shop import gtpShop


def setSecKill(days=None, discount=None):
    data = {
        "model": "{uid:1651950521297552641,"
                 "assignUserIds:[],"
                 "userId:4151410,"
                 "\"startDateTime\":\"{}\","
                 "\"endDateTime\":\"{}\","
                 "\"title\":\"\","
                 "\"productName\":null,"
                 "\"productUid\":\"826329882675187341\","
                 "\"seckillPrice\":{},"
                 "\"maxProductNumber\":\"80\","
                 "\"confirmPeriod\":\"\","
                 "\"maxBuyNumber\":\"5\","
                 "\"autoCancelTime\":\"10\","
                 "\"crossStoreWriteOff\":\"1\","
                 "\"targetType\":\"0\","
                 "\"newCustomerLimitable\":\"0\","
                 "\"groupWay\":\"2\","
                 "\"enabled\":1,"
                 "payMethodLimit:\"7\"}"
    }
    url = 'https://beta47.pospal.cn/EshopMarketing/SaveSeckillRule'
    resp = gtpShop.pos.session.post(url=url, data=data)
    print(resp.content)


setSecKill()
