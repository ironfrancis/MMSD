import json

import requests
from bs4 import BeautifulSoup
import time


# from fake_useragent import UserAgent
# ua = UserAgent()
# print(ua.random)

def searchDangDang(keyword):
    url = 'http://search.dangdang.com/?key=' + keyword + '&act=input'
    r = requests.get(url)
    # print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')

    # discounts = soup.find_all('span', class_='search_discount')
    # for discount in discounts:
    #     print(discount.get_text())
    #
    # products = soup.find_all('span', class_='search_pre_price')
    # priceList= []
    # for p in products:
    #     priceList.append(float(p.get_text().replace('¥', '')))

    productTable = soup.find('div', dd_name="普通商品区域")
    # print(productTable)
    # print("-----------------")
    aList = productTable.find_all('a', class_='pic')
    # for a in aList:
    #     print(a)
    #     print(a.get('title'))
    src = "http:" + aList[0].find('img').get('src')
    print(src)
    with open("/Users/mengmeng/Documents/MMSD V0.2/WebApi/pics/{}.jpg".format(keyword), 'wb') as f:
        f.write(requests.get(src).content)
        f.close()


# 从当当网获取主图
def GetDangDangPicture(keyword):
    url = 'http://search.dangdang.com/?key=' + keyword
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    productTable = soup.find('div', dd_name="普通商品区域")
    a = productTable.find('a', class_='pic')
    pageUrl = "http:" + a.get('href')
    # print(pageUrl)
    cookies = '__permanent_id=20210928203139028313122190090328867; __rpm=%7Cp_699559869...1651815027478; dangdang.com=email=MTgwMTQxNTE0NTc0NDkyNUBkZG1vYmlscGhvbmVfX3VzZXIuY29t&nickname=s6y45w==&display_id=9315920475885&customerid=CSql5wEizB9O2NAI2V+Bxg==&viptype=&show_name=180%2A%2A%2A%2A1457; ddoy=email=1801415145744925%40ddmobilphone__user.com&nickname=%B3%AC%B8%E7&validatedflag=0&agree_date=1; order_follow_source=-%7C-O-123%7C%2311%7C%23login_third_qq%7C%230%7C%23; dest_area=country_id%3D9000%26province_id%3D111%26city_id%3D0%26district_id%3D0%26town_id%3D0; LOGIN_TIME=1651815005046; ddscreen=2; __visit_id=20220506132745671391682334521918944; __out_refer=1651814866%7C!%7Ccn.bing.com%7C!%7C; __trace_id=20220506133027570835219312378804728; search_passback=b7705e8fb89876ee73b27462fc010000bca6680057b27462; pos_9_end=1651814885330; ad_ids=2723462%2C3554379%7C%231%2C1; login.dangdang.com=.AYH=&.ASPXAUTH=xJXv+1oEdLibbkU3lGWeQm9D3Kn2vrCH1wC7GirFHj8FkrZ7gZPu1w==; sessionID=pc_5bdee416907ad68de5a79e19e004e69458c58aa3d56a5ab60f1784fd84b8f1e1; pos_6_start=1651815005366; pos_6_end=1651815005374'

    page = requests.get(url=pageUrl, headers={
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.1.4pre) Gecko/20070510 BonEcho/2.0.0.4pre',
        'Referer': 'http://search.dangdang.com/?key=%E7%94%B5%E8%A7%86%E5%AD%90&act=input',
        'Connection': 'keep-alive',
        'Cookie': cookies

    })
    soup = BeautifulSoup(page.text, 'html.parser')
    src = "http:" + soup.find('div', class_='big_pic').find('img').get('src')
    pic = requests.get(src).content
    print(len(pic))
    print("-----------------")
    with open("/Users/mengmeng/Documents/MMSD V0.2/WebApi/pics/{}.jpg".format(keyword), 'wb') as f:
        f.write(pic)
        f.close()


# 使用qq登录
def loginDD(username, password):
    url = 'http://union.dangdang.com/transfer_inner.php?ad_id=login_third_qq&sys_id=11&backurl=http://www.dangdang.com/'
    session = requests.Session()
    resp = session.get(url)


