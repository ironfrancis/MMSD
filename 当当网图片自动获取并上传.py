import time

from shop_test import gtpShop,syhShop
from dangdang import GetDangDangPicture

table = gtpShop.pos.LoadMatchProductsByPage()
noPicList = table[table['系统内图片'] == 0.0].index.tolist()
print(len(noPicList))
for barcode in noPicList[:70]:
    if barcode[:4] != '9787':
        noPicList.remove(barcode)
    else:
        # 检查目录下是否有图片，目录为：/Users/mengmeng/Documents/MMSD V0.2/WebApi/pics/已上传/
        # 文件名为barcode 如果有，则跳过
        try:
            check_img = open('/Users/mengmeng/Documents/MMSD V0.2/WebApi/pics/已上传/' + barcode + '.jpg', 'rb')
            print('已上传图片：' + barcode)
            continue
        except:
            time.sleep(1)
            try:
                GetDangDangPicture(barcode)
            except:
                continue
