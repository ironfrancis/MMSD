import requests


# 获取总店账号的银豹后台session
def get_zd_session():
    url = 'https://beta47.pospal.cn/account/SignIn?noLog='
    headers = {
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/75.0.3770.100 Safari/537.36',
                  'Referer': 'https://beta47.pospal.cn',
                  'Connection': 'keep-alive',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                  'Upgrade-Insecure-Requests': '1',
              },
    data = {
        'userName': 'mmsd18014151457',
        'password': 'francis003718',
        'returnUrl': '',
        'screenSize': '2560*1440'
    }
    temp_session = requests.session()
    temp_session.post(url, data=data)
    return temp_session  # 返回一个session   可以直接用于后续的请求


# 账号的银豹后台session
def get_gtp_session():
    url = 'https://beta47.pospal.cn/account/SignIn?noLog='
    headers = {
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/75.0.3770.100 Safari/537.36',
                  'Referer': 'https://beta47.pospal.cn',
                  'Connection': 'keep-alive',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                  'Upgrade-Insecure-Requests': '1',
              },
    data = {
        'userName': 'mmsd18014151458',
        'password': 'francis003718',
        'returnUrl': '',
        'screenSize': '2560*1440'
    }
    temp_session = requests.session()
    temp_session.post(url, data=data)
    return temp_session  # 返回一个session   可以直接用于后续的请求
