from Shop import Shop
shop_list = [('萌萌书店(关天培店)', '18014151458', '4151410'), ('萌萌书店(山阳湖店)', '18014151459', '4455361')]
# 实例化2个商店
gtpShop = Shop(shop_list[0][0], shop_list[0][1], shop_list[0][2])
syhShop = Shop(shop_list[1][0], shop_list[1][1], shop_list[1][2])


gtpShop.productDailyCheck(to_html=True)
syhShop.productDailyCheck(to_typora=True)

