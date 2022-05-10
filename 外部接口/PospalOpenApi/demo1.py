import requests
import json
from datetime import datetime
import time
import hashlib

m = hashlib.md5()

hostport = 'https://area47-win.pospal.cn:443/'
appid = '59615CB6F61DB9C562BA42963BF53154'
appKey = '792267275467640925'

# dataJson = {
#     "appId": appid,
#     "postBackParameter": {
#         "parameterType": "",
#         "parameterValue": ""
#     },
# }

dataJson = {
    "appId": appid,
    "barcode": '9787572226427'
}

sign = appKey + json.dumps(dataJson)
# 对sign 进行MD5加密,并转换成大写
sign = hashlib.md5(sign.encode('utf-8')).hexdigest().upper()

# t = str(int(round(time.time() * 1000)))
# 获取当前unix时间戳
t = str(int(round(time.time() * 1000, 0)))
headers = {
    'User-Agent': 'openApi',
    'Content-Type': 'application/json; charset=utf-8',
    'accept-encoding': 'gzip, deflate',
    'time-stamp': "{}".format(t),
    'data-signature': "{}".format(sign),

}
#
# resp = requests.post((hostport + 'pospal-api2/openapi/v1/productOpenApi/queryProductByBarcode'), headers=headers,
#                      json=dataJson)
#
# print(resp.text)


def apitimes_limit():
    t = str(int(round(time.time() * 1000, 0)))  # 获取当前unix时间戳
    data = {
        "appId": appid,
    }
    url = hostport + 'pospal-api2/openapi/v1/openApiLimitAccess/queryAccessTimes'
    sign = appKey + json.dumps(data)
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest().upper()
    headers = {
        'User-Agent': 'openApi',
        'Content-Type': 'application/json; charset=utf-8',
        'accept-encoding': 'gzip, deflate',
        'time-stamp': "{}".format(t),
        'data-signature': "{}".format(sign),
    }

    resp = requests.post(url, headers=headers, json=data)
    print(resp.text)
    return None


# apitimes()

# 查询访问量：
def check_api_logs():
    t = str(int(round(time.time() * 1000, 0)))  # 获取当前unix时间戳
    data = {
        "appId": appid,
        "beginDate": "2022-04-15",
        "endDate": "2022-04-16",
    }
    url = hostport + 'pospal-api2/openapi/v1/openApiLimitAccess/queryDailyAccessTimesLog'
    sign = appKey + json.dumps(data)
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest().upper()
    headers = {
        'User-Agent': 'openApi',
        'Content-Type': 'application/json; charset=utf-8',
        'accept-encoding': 'gzip, deflate',
        'time-stamp': "{}".format(t),
        'data-signature': "{}".format(sign),
    }

    resp = requests.post(url, headers=headers, json=data)
    print(resp.text)
    return None


check_api_logs()
