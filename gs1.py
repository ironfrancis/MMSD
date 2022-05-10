import json
from bs4 import BeautifulSoup

import requests


def searchGs1ByJson(barcode):
    url = 'https://bff.gds.org.cn/gds/searching-api/ProductService/ProductListByGTIN?PageSize=30&PageIndex=1' \
          '&SearchItem=%s' % barcode
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.149 Safari/537.36 ',
        'Referer': 'https://www.gds.org.cn/',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkQzQ0QzQzYxRjYyMjE0N0U3MUZDODM2NDI3RDRFOUVGM0M5QzM2RUZSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6IjA4MDhZZllpRkg1eF9JTmtKOVRwN3p5Y051OCJ9.eyJuYmYiOjE2NTE5MDM4NjcsImV4cCI6MTY1MTkwNzQ2NywiaXNzIjoiaHR0cHM6Ly9wYXNzcG9ydC5nZHMub3JnLmNuIiwiY2xpZW50X2lkIjoidnVlanNfY29kZV9jbGllbnQiLCJzdWIiOiIxODkxNDcwIiwiYXV0aF90aW1lIjoxNjUxOTAzODY1LCJpZHAiOiJsb2NhbCIsInJvbGUiOiJNaW5lIiwiVXNlckluZm8iOiJ7XCJVc2VyTmFtZVwiOm51bGwsXCJCcmFuZE93bmVySWRcIjowLFwiQnJhbmRPd25lck5hbWVcIjpudWxsLFwiR2NwQ29kZVwiOm51bGwsXCJVc2VyQ2FyZE5vXCI6XCLmmoLml6Dkv6Hmga9cIixcIklzUGFpZFwiOmZhbHNlLFwiQ29tcGFueU5hbWVFTlwiOm51bGwsXCJDb21wYW55QWRkcmVzc0NOXCI6bnVsbCxcIkNvbnRhY3RcIjpudWxsLFwiQ29udGFjdFRlbE5vXCI6bnVsbCxcIkdjcExpY2Vuc2VIb2xkZXJUeXBlXCI6bnVsbCxcIkxlZ2FsUmVwcmVzZW50YXRpdmVcIjpudWxsLFwiVW5pZmllZFNvY2lhbENyZWRpdENvZGVcIjpudWxsfSIsIlY0VXNlckluZm8iOiJ7XCJVc2VyTmFtZVwiOlwiQnJlZXplLkZyb3N0YWtcIixcIkVtYWlsXCI6bnVsbCxcIlBob25lXCI6XCIxODAxNDE1MTQ1N1wiLFwiQ2FyZE5vXCI6XCJcIn0iLCJqdGkiOiI5MUZCN0U4RjEyNTU1RkMzQzM1QjIzRUJFNjIzQ0Q4MiIsInNpZCI6IjEwQzI0M0NBQjM1ODY4NTFGMUUxNDAzRUQzQjA2NDNCIiwiaWF0IjoxNjUxOTAzODY3LCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIiwiYXBpMSIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJwd2QiXX0.eg-v2jiIzo-xVjRlp7rQMWk0FMUEWxFOd1CKYUfRax113i3DzORPIf_aX3eoUC-uXUaSBpCdRQrS7l8l0xAiC-irRaw5km2pXH-H1cwubGw0FqIZx0XU1dSyqYnunumhRhXGQI8bNU7aYQNYOrAovBTg9InF3PsedgZolHzavNLPWSkww-9uPcRDe0FmdaxYXIHVppFnqPy_r9xXTDJDqb4zAUvZVCbPcHADxQH0GhVE5M7SaLIZeW7VMDckRwNsE2sLwPvk9ALeDAB9D3IbClr_dww9VL8gWVBq-80fwbIk-ALKJg6kHjWXy3CZxHfaKpjAlXjn2yvUq8v93tL6sQ'
    }
    resp = requests.get(url, headers=headers)
    r = resp.json()
    if r['Msg'] == 'Success':
        print("连接gs1成功！")
        if r['Data']['TotalCount'] == 0:
            print("{} 该条码错误或没有备案！".format(barcode))
        else:
            print("找到匹配商品")
            data = r['Data']['Items'][0]
            resultDict = dict(
                pBrand=data['brandcn'],
                pName=data['description'],
                pCategory=data['gpcname'],
                # gtin=data['gtin'],
                # f_id=data['f_id'],
                adName=(data['brandcn'] + ' ' + data['description'])
            )
            return resultDict
    else:
        print("无法连接gs1服务器")
        print(r)


def ProductInfoByGTIN(barcode):
    pDict = searchGs1ByJson(barcode)
    print(pDict)
    url = 'https://bff.gds.org.cn/gds/searching-api/ProductService/ProductInfoByGTIN?gtin={}&id={}'.format(
        pDict['gtin'], pDict['f_id']
    )
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.149 Safari/537.36 ',
        'Referer': 'https://www.gds.org.cn/',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Authorization': 'Bearer '
                         'eyJhbGciOiJSUzI1NiIsImtpZCI6IkQzQ0QzQzYxRjYyMjE0N0U3MUZDODM2NDI3RDRFOUVGM0M5QzM2RUZSUzI1NiIsI'
                         'nR5cCI6ImF0K2p3dCIsIng1dCI6IjA4MDhZZllpRkg1eF9JTmtKOVRwN3p5Y051OCJ9.eyJuYmYiOjE2NTE4NTA3MzgsIm'
                         'V4cCI6MTY1MTg1NDMzOCwiaXNzIjoiaHR0cHM6Ly9wYXNzcG9ydC5nZHMub3JnLmNuIiwiY2xpZW50X2lkIjoidnVlan'
                         'NfY29kZV9jbGllbnQiLCJzdWIiOiIxODkxNDcwIiwiYXV0aF90aW1lIjoxNjUxODUwNzM4LCJpZHAiOiJsb2NhbCIsIn'
                         'JvbGUiOiJNaW5lIiwiVXNlckluZm8iOiJ7XCJVc2VyTmFtZVwiOm51bGwsXCJCcmFuZE93bmVySWRcIjowLFwiQnJhbmR'
                         'Pd25lck5hbWVcIjpudWxsLFwiR2NwQ29kZVwiOm51bGwsXCJVc2VyQ2FyZE5vXCI6XCLmmoLml6Dkv6Hmga9cIixcIklz'
                         'UGFpZFwiOmZhbHNlLFwiQ29tcGFueU5hbWVFTlwiOm51bGwsXCJDb21wYW55QWRkcmVzc0NOXCI6bnVsbCxcIkNvbnRhY'
                         '3RcIjpudWxsLFwiQ29udGFjdFRlbE5vXCI6bnVsbCxcIkdjcExpY2Vuc2VIb2xkZXJUeXBlXCI6bnVsbCxcIkxlZ2FsUm'
                         'VwcmVzZW50YXRpdmVcIjpudWxsLFwiVW5pZmllZFNvY2lhbENyZWRpdENvZGVcIjpudWxsfSIsIlY0VXNlckluZm8iOiJ'
                         '7XCJVc2VyTmFtZVwiOlwiQnJlZXplLkZyb3N0YWtcIixcIkVtYWlsXCI6bnVsbCxcIlBob25lXCI6XCIxODAxNDE1MTQ1'
                         'N1wiLFwiQ2FyZE5vXCI6XCJcIn0iLCJqdGkiOiJEMDI1MkQ0Q0I3Qjk1QjdGMTZGQjBGODRBQzgyNEE0RiIsInNpZCI6I'
                         'jBBRjA5NjlBMjY0NTBFRDlFQjlCOEYyNENENTE4OTQyIiwiaWF0IjoxNjUxODUwNzM4LCJzY29wZSI6WyJvcGVuaWQiLC'
                         'Jwcm9maWxlIiwiYXBpMSIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJwd2QiXX0.XTFxXPUeeu68H4Dx_TuZHO553vw'
                         'MiAfUZ5roJGbsqxLu5EUtgndwaQeZfwSjPDZt4FyAtNApTKFWs-lA3Xeyk7oPjrCl8EnJfgKJUIs41RuWjL1ADbMNJLYq'
                         'WyqIfZdO1yiU1_MfILPpXdsC4nUhmfORFl_R0FxcPCtUsrcUCbWeR4A2xe-E0J57O4Qs-Wx4_AawT4YWmUrUUAPVeybwJ'
                         'Uo1m-utduIolm3IX9daFwiWb1Uu7mX-1QzXc1B4si5JMqNwgYOBr3vtbleIec9w4m03avXck9ieLbKTsamA6pebtluYJK'
                         'nxiMCNoiER-fgfnHQhoSdzdObH-WQBSiU1rA ',
    }
    resp = requests.get(url, headers=headers)
    print(resp.text)


def searchGs1BySite(barcode):
    url = 'https://www.gds.org.cn/#/barcodeList/index?type=barcode&keyword=' + str(barcode)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.149 Safari/537.36 ',
        'Referer': 'https://www.gds.org.cn/',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkQzQ0QzQzYxRjYyMjE0N0U3MUZDODM2NDI3RDRFOUVGM0M5QzM2RUZSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6IjA4MDhZZllpRkg1eF9JTmtKOVRwN3p5Y051OCJ9.eyJuYmYiOjE2NTE5MDM4NjcsImV4cCI6MTY1MTkwNzQ2NywiaXNzIjoiaHR0cHM6Ly9wYXNzcG9ydC5nZHMub3JnLmNuIiwiY2xpZW50X2lkIjoidnVlanNfY29kZV9jbGllbnQiLCJzdWIiOiIxODkxNDcwIiwiYXV0aF90aW1lIjoxNjUxOTAzODY1LCJpZHAiOiJsb2NhbCIsInJvbGUiOiJNaW5lIiwiVXNlckluZm8iOiJ7XCJVc2VyTmFtZVwiOm51bGwsXCJCcmFuZE93bmVySWRcIjowLFwiQnJhbmRPd25lck5hbWVcIjpudWxsLFwiR2NwQ29kZVwiOm51bGwsXCJVc2VyQ2FyZE5vXCI6XCLmmoLml6Dkv6Hmga9cIixcIklzUGFpZFwiOmZhbHNlLFwiQ29tcGFueU5hbWVFTlwiOm51bGwsXCJDb21wYW55QWRkcmVzc0NOXCI6bnVsbCxcIkNvbnRhY3RcIjpudWxsLFwiQ29udGFjdFRlbE5vXCI6bnVsbCxcIkdjcExpY2Vuc2VIb2xkZXJUeXBlXCI6bnVsbCxcIkxlZ2FsUmVwcmVzZW50YXRpdmVcIjpudWxsLFwiVW5pZmllZFNvY2lhbENyZWRpdENvZGVcIjpudWxsfSIsIlY0VXNlckluZm8iOiJ7XCJVc2VyTmFtZVwiOlwiQnJlZXplLkZyb3N0YWtcIixcIkVtYWlsXCI6bnVsbCxcIlBob25lXCI6XCIxODAxNDE1MTQ1N1wiLFwiQ2FyZE5vXCI6XCJcIn0iLCJqdGkiOiI5MUZCN0U4RjEyNTU1RkMzQzM1QjIzRUJFNjIzQ0Q4MiIsInNpZCI6IjEwQzI0M0NBQjM1ODY4NTFGMUUxNDAzRUQzQjA2NDNCIiwiaWF0IjoxNjUxOTAzODY3LCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIiwiYXBpMSIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJwd2QiXX0.eg-v2jiIzo-xVjRlp7rQMWk0FMUEWxFOd1CKYUfRax113i3DzORPIf_aX3eoUC-uXUaSBpCdRQrS7l8l0xAiC-irRaw5km2pXH-H1cwubGw0FqIZx0XU1dSyqYnunumhRhXGQI8bNU7aYQNYOrAovBTg9InF3PsedgZolHzavNLPWSkww-9uPcRDe0FmdaxYXIHVppFnqPy_r9xXTDJDqb4zAUvZVCbPcHADxQH0GhVE5M7SaLIZeW7VMDckRwNsE2sLwPvk9ALeDAB9D3IbClr_dww9VL8gWVBq-80fwbIk-ALKJg6kHjWXy3CZxHfaKpjAlXjn2yvUq8v93tL6sQ'
    }
    r = requests.get(url=url,headers=headers)
    # with open("test.html",'w') as f:
    #     f.write(r.text)
    print(r.text)

# SearchGs1ByJson(6953787375103)
# ProductInfoByGTIN(9973493720995)

# searchGs1BySite(6953787375103)