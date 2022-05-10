from BaseClass.Shop import gtpShop
import requests
import bs4
import re
import difflib


def getPagePic(barcode, url):
    resp = requests.get(url=url)
    try:
        check_img = open('/Users/mengmeng/Documents/MMSD V0.2/WebApi/pics/已上传/' + barcode + '.jpg', 'rb')
        print('已上传图片：' + barcode)
        return None
    except:
        with open('/Users/mengmeng/Documents/MMSD V0.2/WebApi/pics/' + barcode + '.jpg', 'wb') as f:

            f.write(resp.content)
        return print("图片已保存")


# 根据keyword=得力 查询商品库，并获取图片，保存本地
def brandPicFix():
    # table = syhShop.pos.LoadAddvancedProductsForBatchUpdate(brand='1600950043480405088')
    table = gtpShop.pos.LoadProductsByPage(nums=10000, keyword="得力")
    # table = gtpShop.pos.LoadMatchProductsByPage(keyword="得力")
    # print(tabel.商品名称.unique())
    for i in range(table.shape[0]):
        pName = table.loc[i]['商品名称']
        # 提取pName中的货号，\d{3,8
        try:
            pCode = str(re.search(r'\d{3,8}', pName).group())
            print(pName, pCode)
            url = "https://www.nbdeli.com/search.html?search=" + pCode
        # 提取不到货号的直接跳过
        except:
            print(pName, '货号提取失败 ', table.loc[i, '条码'])
            continue

        # 请求网站，使用bs4解析 true-img （大图 800*800）
        resp = requests.get(url)
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')
        pId = str(table.loc[i]['条码'])
        print(pId, pName)
        # print(soup)
        imgs = soup.find_all('img', class_='true-img')
        if len(imgs) == 1:
            print("可以定位到商品")
            imgPath = imgs[-1]['src']
            getPagePic(barcode=pId, url=imgPath)
        elif len(imgs) > 0:
            print("共计找到 ", len(imgs), " 张图片，开始进行名称匹配。。。")
            imgDict = {}
            for i in range(len(imgs)):
                imgName = imgs[i]['alt']
                # print(imgName)
                diff = round(difflib.SequenceMatcher(None, pName, imgName).quick_ratio(), 3)
                # print(diff)
                imgDict[str(i)] = diff
            imgDict = sorted(imgDict.items(), key=lambda x: x[1], reverse=True)
            if float(imgDict[0][1]) > 0.3:
                bestNo = imgDict[0][0]
                print("最佳匹配度:", imgDict[0][1], "开始写入图片")
                getPagePic(barcode=pId, url=imgs[int(bestNo)]['src'])
            else:
                print("没有合适的匹配项目")

        else:
            print("没有找到图片！")
        print(("-" * 20))


brandPicFix()
